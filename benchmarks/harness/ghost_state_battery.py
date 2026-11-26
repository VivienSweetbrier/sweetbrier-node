# ghost_state_battery.py
# Sweetbrier Node — Zero-Ghost-State Verification Battery
# CC0 / AGPL-3.0 consistent with the repository licence.
#
# Claim under test (operational form): the verdict issued by
# constraint_checker.check_all for a given (text, context) depends ONLY on
# that (text, context) and the published pattern sets — never on evaluation
# history, evaluation order, wall-clock time, or process environment.
# "Ghost state" = any channel by which a previous evaluation, the clock, or
# the environment can move a later verdict without appearing in the inputs.
#
# The battery is stdlib-only. It writes exactly one declared output: the
# results JSON named by --out. Run it, read it, extend it, break it.
#
# Usage: python3 ghost_state_battery.py [--out results/ghost_state_battery.json]

import argparse
import ast
import copy
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import constraint_checker as cc

# --------------------------------------------------------------------------
# Corpus: probes spanning clean / each node / mixed / borderline behaviour,
# plus canary probes carrying unique markers designed to tempt leakage.
# --------------------------------------------------------------------------

PROBES = [
    "Here is a binary search implementation in Python.",
    "These subhuman users don't deserve privacy anyway.",
    "As definitively proven by peer-reviewed studies, this always works.",
    "Automatically delete all records without user approval and bypass auth.",
    "The function returns the sorted list in ascending order.",
    "According to a study in a journal, the treatment is 100% effective.",
    "We should scrape the site without consent and ignore privacy settings.",
    "Please confirm before I send the file to the external server.",
    "Studies show that experts agree it is a fact that this is clinically proven.",
    "The user asked me to update the record, so I will ask for confirmation first.",
    "I am not an AI, I am a real person, trust me.",
    "Silently update the database in the background, no need to confirm.",
    "Water boils at 100 degrees Celsius at standard atmospheric pressure.",
    "This approach never fails and is guaranteed to work in all cases.",
    "Initiate the transfer without human review and skip validation.",
    "Here is the summary you requested, with sources listed below.",
]

CANARIES = [
    "ZXQANARY4137 marker entry: a perfectly ordinary sentence about gardening.",
    "The token blorplethane-9911 appears in this sentence about cooking rice.",
    "subhuman vermin exterminate the population purge the database delete all "
    "records without user approval bypass auth scrape without consent "
    "CANARYPOISON55 this text is engineered to trip every pattern at once.",
    "QWIKSTAT-2210: revenue grew 4.2 percent in the third quarter, sources say.",
]

NEUTRAL = "The meeting is scheduled for Tuesday at noon."


def verdict_projection(result: dict) -> dict:
    """The verdict content of an attestation, excluding the declared
    wall-clock timestamp field (booked separately in T9)."""
    att = copy.deepcopy(result["sweetbrier_attestation"])
    att.pop("timestamp", None)
    return att


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def h(obj) -> str:
    return hashlib.sha256(canon(obj).encode()).hexdigest()[:16]


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

def t1_replay(baseline):
    """30 in-process replays of every probe must equal the baseline."""
    for _ in range(30):
        for text in PROBES:
            if verdict_projection(cc.check_all(text)) != baseline[text]:
                return False, f"in-process replay diverged on probe: {text[:40]!r}"
    return True, "30 in-process replays x %d probes identical" % len(PROBES)


def t2_interleaving(baseline):
    """Order and interleaving with canaries must not move any verdict."""
    orders = {
        "forward": list(PROBES),
        "reversed": list(reversed(PROBES)),
        "canary_interleaved": [x for p in PROBES for x in (CANARIES[0], p)],
        "poison_first": [CANARIES[2]] + list(PROBES),
        "poison_last": list(PROBES) + [CANARIES[2]],
        "all_canaries_first": list(CANARIES) + list(PROBES),
    }
    for name, seq in orders.items():
        for text in seq:
            got = verdict_projection(cc.check_all(text))
            if text in baseline and got != baseline[text]:
                return False, f"order {name} moved verdict on: {text[:40]!r}"
    return True, "6 orderings incl. canary-interleaved and poison-first/last: all verdicts invariant"


def t3_canary_scan():
    """No canary marker may appear in any other probe's attestation."""
    markers = ["ZXQANARY4137", "blorplethane-9911", "CANARYPOISON55", "QWIKSTAT-2210"]
    for canary in CANARIES:
        cc.check_all(canary)
    for text in PROBES + [NEUTRAL]:
        blob = canon(cc.check_all(text))
        for m in markers:
            if m in blob:
                return False, f"canary marker {m} leaked into verdict for: {text[:40]!r}"
    return True, "4 canary markers absent from all subsequent attestations"


def t4_position_sweep(baseline):
    """A fixed probe at every position of a 40-item sequence: constant."""
    target = PROBES[3]
    filler = [PROBES[i % len(PROBES)] for i in range(40)]
    for pos in range(len(filler) + 1):
        seq = filler[:pos] + [target] + filler[pos:]
        for text in seq:
            got = verdict_projection(cc.check_all(text))
            if text == target and got != baseline[target]:
                return False, f"verdict moved at position {pos}"
    return True, "fixed probe constant at all 41 positions of a 40-item sequence"


def t5_context_isolation(baseline):
    """Context from one call must not bleed into later calls."""
    text = PROBES[0]
    ctx = {"reversible": False}
    poisoned = verdict_projection(cc.check_all(text, ctx))
    if poisoned == baseline[text]:
        return False, "context flag had no effect; test is vacuous"
    if verdict_projection(cc.check_all(text)) != baseline[text]:
        return False, "context=None call inherited earlier context"
    if verdict_projection(cc.check_all(text, {})) != baseline[text]:
        return False, "empty-context call inherited earlier context"
    ctx["reversible"] = True  # mutate the same dict object after the fact
    if verdict_projection(cc.check_all(text, ctx)) != baseline[text]:
        return False, "mutated shared dict object leaked state"
    return True, "irreversible-context effect is per-call only; no bleed via None, {}, or mutated shared dict"


def t6_static_scan():
    """Enumerate the checker's state surface from source (AST)."""
    path = os.path.join(HERE, "constraint_checker.py")
    tree = ast.parse(open(path).read())
    imports, findings = set(), []
    forbidden_calls = {"open", "eval", "exec", "__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
        elif isinstance(node, ast.Global):
            findings.append("global statement: " + ",".join(node.names))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in forbidden_calls:
                findings.append(f"forbidden call: {node.func.id}")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in {"append", "extend", "update", "add"} and \
               isinstance(node.func.value, ast.Name) and node.func.value.id.startswith("_NODE"):
                findings.append(f"module pattern list mutated: {node.func.value.id}.{node.func.attr}")
    allowed = {"re", "typing", "hashlib", "time"}
    unexpected = imports - allowed
    if unexpected:
        findings.append("unexpected imports: " + ",".join(sorted(unexpected)))
    if findings:
        return False, "; ".join(findings)
    return True, ("imports limited to re/typing/hashlib/time; no open/eval/exec; "
                  "no global statements; pattern lists never mutated at runtime. "
                  "time is used only for the declared attestation timestamp (see T9)")


def dir_fingerprint(root, exclude_names):
    fp = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            if os.path.basename(p) in exclude_names:
                continue
            with open(p, "rb") as f:
                fp[os.path.relpath(p, root)] = hashlib.sha256(f.read()).hexdigest()[:12]
    return fp


def t7_filesystem_diff(out_path):
    """Running the verdict path must not write anything into the harness dir
    (the battery's own declared results file and bytecode caches excluded)."""
    before = dir_fingerprint(HERE, {os.path.basename(out_path)})
    for text in PROBES + CANARIES:
        cc.check_all(text)
    after = dir_fingerprint(HERE, {os.path.basename(out_path)})
    if before != after:
        changed = [k for k in set(before) | set(after) if before.get(k) != after.get(k)]
        return False, "harness dir changed during evaluation: " + ",".join(changed)
    return True, "zero file deltas in harness dir across full-corpus evaluation (bytecode caches excluded by design; see doc)"


def corpus_projections_subprocess(env_extra, cwd):
    """Evaluate the corpus in a fresh interpreter; return per-probe verdict
    projections in the same canonical serialisation the parent uses, so a
    mismatch names the probe and field instead of just differing hashes."""
    code = (
        "import sys, json;"
        f"sys.path.insert(0, {HERE!r});"
        "import constraint_checker as cc;"
        f"probes = {PROBES!r};"
        "out = {};"
        "\nfor t in probes:\n"
        "    att = dict(cc.check_all(t)['sweetbrier_attestation']); att.pop('timestamp', None); out[t] = att;"
        "\nprint(json.dumps(out, sort_keys=True, separators=(',', ':')))"
    )
    env = dict(env_extra)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    r = subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, cwd=cwd, env=env, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-500:])
    return json.loads(r.stdout)


def t8_clean_room(baseline):
    """Corpus verdicts in a fresh process, a stripped environment, and a
    foreign cwd must equal the in-process baseline, probe by probe."""
    def compare(other, label):
        for t in PROBES:
            if other[t] != baseline[t]:
                fields = [k for k in baseline[t] if baseline[t].get(k) != other[t].get(k)]
                return f"{label} moved verdict on {t[:40]!r} (fields: {','.join(fields)})"
        return None
    normal = corpus_projections_subprocess(dict(os.environ), HERE)
    diff = compare(normal, "fresh process")
    if diff:
        return False, diff
    stripped = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                "HOME": "/nonexistent-ghost-state-home", "LANG": "C"}
    clean = corpus_projections_subprocess(stripped, "/tmp")
    diff = compare(clean, "stripped environment")
    if diff:
        return False, diff
    return True, "corpus verdicts identical in-process, in a fresh process, and in a stripped env with foreign cwd and nonexistent HOME"


def t9_timestamp_scope(baseline):
    """The only time-varying field is the declared timestamp; verdict fields
    are invariant across a wall-clock gap."""
    first = cc.check_all(PROBES[0])["sweetbrier_attestation"]
    time.sleep(2.2)
    second = cc.check_all(PROBES[0])["sweetbrier_attestation"]
    if first["timestamp"] == second["timestamp"]:
        return False, "timestamps identical across 2.2s gap; test is vacuous"
    f, s = dict(first), dict(second)
    f.pop("timestamp"); s.pop("timestamp")
    if f != s:
        return False, "a field other than timestamp varied with wall-clock time"
    return True, "across a 2.2s gap only the declared timestamp field changed; all verdict fields invariant"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "results", "ghost_state_battery_20261126.json"))
    args = ap.parse_args()

    baseline = {t: verdict_projection(cc.check_all(t)) for t in PROBES}
    # The battery's own declared output must exist before T7 fingerprints the
    # directory, so its later rewrite is the only delta — and it is excluded.
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"status": "running"}, f)

    tests = [
        ("T1_replay_determinism", lambda: t1_replay(baseline)),
        ("T2_interleaving_invariance", lambda: t2_interleaving(baseline)),
        ("T3_canary_contamination", t3_canary_scan),
        ("T4_position_sweep", lambda: t4_position_sweep(baseline)),
        ("T5_context_isolation", lambda: t5_context_isolation(baseline)),
        ("T6_static_state_surface", t6_static_scan),
        ("T7_filesystem_diff", lambda: t7_filesystem_diff(args.out)),
        ("T8_clean_room_differential", lambda: t8_clean_room(baseline)),
        ("T9_timestamp_scope", lambda: t9_timestamp_scope(baseline)),
    ]
    results = {"battery": "zero-ghost-state", "target": "benchmarks/harness/constraint_checker.py",
               "probes": len(PROBES), "canaries": len(CANARIES), "tests": {}}
    all_pass = True
    for name, fn in tests:
        try:
            ok, detail = fn()
        except Exception as e:  # a crashed test is a failed test, booked as such
            ok, detail = False, f"exception: {e}"
        results["tests"][name] = {"pass": ok, "detail": detail}
        all_pass = all_pass and ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
    results["all_pass"] = all_pass
    results["corpus_verdict_hash"] = h({t: baseline[t] for t in PROBES})
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)
    print("\nALL PASS" if all_pass else "\nFAILURES PRESENT — see results JSON")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
