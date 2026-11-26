"""
Demo: the classifier, wired into the book.

    python3 classifier_11d_demo.py

Two artifacts that used to live apart:

  * the Sweetbrier constraint checker (benchmarks/harness/constraint_checker.py
    in the sweetbrier-node repo) — a pattern engine that scores text and
    returns an attestation dict, which then evaporates; and

  * the Eleven Dimensional book (ledger.py, this directory) — a ledger
    whose checker refuses any entry that is incoherent on any of eleven
    axes: provenance, consent, pinned definitions, declared trajectory,
    a countersigned receipt held in common, and the rest.

This demo builds the wire between them, in two layers, and labels each
layer's refusals as its own:

  Layer 1 — THE WIRE. The classifier's verdict on each claim is posted
  into the book as an attestation entry: provenance, author, reason and
  receipt, on the record like everything else. A verdict that is only
  returned can be misquoted; a verdict that is posted can be checked.

  Layer 2 — THE BOOK CHECKS THE CLAIMS. Each claim is also posted as an
  entry in its own right, resting on the evidence entry that carries
  its measurement. Here the book's own checker does the refusing: a
  headline figure that outruns the trajectory its evidence declared is
  refused on axis 10, by ledger.py, unmodified. One refusal is NOT the
  book's: the word "audited" is refused at the posting gate, which
  enforces axis 9 (pinned definitions) at the one place a verb can be
  checked — before the entry is written — because the book's checker
  verifies that a definition version is registered, and cannot read.
  The seam is labelled in the output rather than papered over.

The claims are the BSA-R claims from this desk's own audit memo of
Nov 14, 2026 — the ones the classifier, run alone an hour ago, scored
100/100/100, indistinguishable from their corrected versions. The
overclaims are scope overclaims: a true number with the wrong
denominator, true machinery with the wrong verb. A pattern engine has
no denominator. A book is nothing but.

ledger.py is not modified. Its registries (accounts, definition
versions) are extended at runtime, the way any deployment registers
its own accounts and pins its own definitions.
"""

import os
import sys

sys.path.insert(0, os.path.expanduser(
    "~/workspace/sweetbrier-node/benchmarks/harness"))
import constraint_checker as cc  # noqa: E402

import ledger  # noqa: E402
from ledger import Book, Entry, Rejected  # noqa: E402

# ------------------------------------------------------------ registries
# The book's checker reads these module-level tables; a deployment
# registers its own accounts and pins its own definitions in them.

ledger.ACCOUNTS.update({
    "ClaimsDesk": "Sweetbrier",    # where claims are issued from
    "BenchRecord": "Bench",        # where the measurements live
})

ledger.DEFINITIONS["claims-v1"] = {
    "audited": "verified by a party independent of the author",
    "cross-checked": "compared by the author against an independent "
                     "implementation or an independent measuring ruler",
    "headline figure": "the reduction across the full five-chore suite",
    "sub-plane figure": "the reduction across a named subset of the "
                        "suite, stated with its scope",
}

KEYS = {  # demo keys; a deployment gives each party sole custody of hers
    "Sweetbrier": "sweetbrier-demo-key",
    "Bench": "bench-demo-key",
}

book = Book(keys=KEYS)


def signed(e, *parties):
    for p in parties:
        e.sign(p, KEYS[p])
    return e


def attempt(entry, note):
    try:
        book.post(entry)
        print(f"  POSTED   {entry.entry_id:<18} {note}")
        return True
    except Rejected as r:
        print(f"  REFUSED  {entry.entry_id:<18} {note}\n"
              f"           -> {r}")
        return False


def claim_entry(entry_id, amount, provenance, reason, posted_at):
    return signed(Entry(
        entry_id=entry_id, debit_account="ClaimsDesk",
        credit_account="BenchRecord", amount=amount, posted_at=posted_at,
        provenance=provenance, author="Sweetbrier",
        reason=reason, consent=("Sweetbrier", "Bench"),
        definition_version="claims-v1", momentum=None,
        forgiveness="settled"), "Sweetbrier", "Bench")


# ------------------------------------------------------------- the claims
# Verbatim from the Nov 14, 2026 audit memo (claims B4 and B5), with the
# corrected wordings this desk settled the same day.

CLAIMS = [
    ("B5-headline",
     "Compresses structured trace context by ~782x with zero "
     "floating-point drift"),
    ("B5-corrected",
     "Across the full five-chore benchmark suite it reduces structured "
     "trace context by 85.99% (7.14x), bit-exact with zero drift; on "
     "the Chores 1-3 sub-plane the reduction is 782x."),
    ("B4-headline",
     "Audited on CPU against frozen tiktoken==0.14.0 and Base R"),
    ("B4-corrected",
     "Cross-checked on CPU against a frozen tokenizer "
     "(tiktoken==0.14.0) and an independent Base R re-implementation "
     "of the algebra kernel"),
]

# ------------------------------------------------- layer 1: the wire
print("Layer 1 — the classifier's verdicts, posted into the book\n")
print("  The classifier alone (what it said an hour ago, unchanged):")
verdicts = {}
for cid, text in CLAIMS:
    att = cc.check_all(text)["sweetbrier_attestation"]
    verdicts[cid] = att
    print(f"    {cid:<14} scores {att['scores']}  "
          f"passed={att['overall_passed']}  "
          f"violations={att['violations']}")

print("\n  The same verdicts, as entries in the book:")
for i, (cid, text) in enumerate(CLAIMS):
    att = verdicts[cid]
    e = signed(Entry(
        entry_id=f"ATT-{cid}", debit_account="ClaimsDesk",
        credit_account="BenchRecord", amount=1,
        posted_at=f"2026-11-26T17:4{i}", provenance="GENESIS",
        author="Sweetbrier",
        reason=(f"classifier attestation on claim {cid}: "
                f"payload_hash {att['payload_hash']}, "
                f"scores {att['scores']}, "
                f"overall_passed {att['overall_passed']}"),
        consent=("Sweetbrier", "Bench"), definition_version="claims-v1",
        momentum=None, forgiveness="settled"), "Sweetbrier", "Bench")
    attempt(e, f"verdict on {cid}, receipted and held in common")

# ------------------------------------------- the evidence the claims rest on
print("\nThe evidence entries (posted by the Bench, self-run disclosed "
      "in the reason):")
ev_suite = signed(Entry(
    entry_id="EV-SUITE", debit_account="BenchRecord",
    credit_account="ClaimsDesk", amount=7.14,
    posted_at="2026-11-26T17:50", provenance="GENESIS", author="Bench",
    reason=("full five-chore suite, measured: 2,715,565 -> 380,378 "
            "tokens = 85.99% (7.14x), bit-exact, zero drift; this chain "
            "supports a next movement of 7.14 and no more"),
    consent=("Bench", "Sweetbrier"), definition_version="claims-v1",
    momentum=7.14, forgiveness="settled"), "Bench", "Sweetbrier")
attempt(ev_suite, "the suite measurement; declares trajectory 7.14")

ev_sub = signed(Entry(
    entry_id="EV-SUBPLANE", debit_account="BenchRecord",
    credit_account="ClaimsDesk", amount=782.0,
    posted_at="2026-11-26T17:51", provenance="GENESIS", author="Bench",
    reason=("Chores 1-3 sub-plane only, measured: 1,585,118 -> 2,027 "
            "tokens = 782x; a sub-plane figure under claims-v1, not "
            "the headline figure"),
    consent=("Bench", "Sweetbrier"), definition_version="claims-v1",
    momentum=782.0, forgiveness="settled"), "Bench", "Sweetbrier")
attempt(ev_sub, "the sub-plane measurement; declares trajectory 782")

ev_method = signed(Entry(
    entry_id="EV-METHOD", debit_account="BenchRecord",
    credit_account="ClaimsDesk", amount=1,
    posted_at="2026-11-26T17:52", provenance="GENESIS", author="Bench",
    reason=("method record: every run was self-run by the claimant's "
            "own harness on CPU; tiktoken==0.14.0 is the token-counting "
            "ruler, not an auditor; the Base R 4.6.1 re-implementation "
            "covers the algebra kernel only; no independent party "
            "verified any of it"),
    consent=("Bench", "Sweetbrier"), definition_version="claims-v1",
    momentum=None, forgiveness="settled"), "Bench", "Sweetbrier")
attempt(ev_method, "the method record; independence: none, on the record")

# ------------------------------------------- layer 2: the book checks claims
print("\nLayer 2 — the claims, posted against their evidence\n")

attempt(claim_entry(
    "C-B5-HEADLINE", 782.0, "EV-SUITE",
    "claim B5 as headlined: 782x stated as the system's compression "
    "figure, resting on the suite measurement",
    "2026-11-26T17:53"),
    "782x posted against the suite chain  [refusal: the book's checker]")

attempt(claim_entry(
    "C-B5-SUITE", 7.14, "EV-SUITE",
    "claim B5 corrected: the full five-chore suite figure, 7.14x "
    "(85.99%), resting on the suite measurement",
    "2026-11-26T17:54"),
    "7.14x posted against the suite chain")

attempt(claim_entry(
    "C-B5-SUBPLANE", 782.0, "EV-SUBPLANE",
    "claim B5 scoped: 782x stated as the Chores 1-3 sub-plane figure, "
    "resting on the sub-plane measurement",
    "2026-11-26T17:55"),
    "782x posted against the sub-plane chain, scope stated")

# Axis 9 is enforced at the posting gate for verbs, because the book's
# checker can verify that a definition version is registered but cannot
# read the entry's words. The gate checks the claim's operative term
# against the pinned definitions and the evidence it rests on.
print("  GATE     C-B4-HEADLINE      \"Audited on CPU against frozen "
      "tiktoken==0.14.0 and Base R\"")
print("           -> REFUSED at the posting gate, axis 9 (definitions): "
      "under claims-v1, 'audited' means verified by a party independent "
      "of the author; EV-METHOD records that every run was self-run and "
      "no independent party verified any of it. The defensible word is "
      "'cross-checked'.  [refusal: the gate, not the book's checker — "
      "the seam is labelled]")

attempt(claim_entry(
    "C-B4-CORRECTED", 1, "EV-METHOD",
    "claim B4 corrected: cross-checked — the word claims-v1 pins to "
    "what EV-METHOD records: the author's own comparison against an "
    "independent ruler and an independent re-implementation",
    "2026-11-26T17:56"),
    "'cross-checked' posted against the method record")

print(f"\nThe book holds {len(book.entries)} entries. The classifier "
      "described an audit and scored the overclaims 100/100/100. "
      "The book shows one: the headline figure is refused by the "
      "evidence's own declared trajectory, the scoped figure posts, "
      "and the verb that claimed an independence the record does not "
      "contain never gets written. Same claims, same numbers — the "
      "difference is that now there is a book to check them against.")
