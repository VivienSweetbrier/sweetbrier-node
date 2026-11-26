# Zero Ghost State — Verification Protocol and First Run

*Added 2026-11-26. The battery is `benchmarks/harness/ghost_state_battery.py` (stdlib only). The machine-readable results of the first run are `benchmarks/harness/results/ghost_state_battery_20261126.json`. Run it yourself; extend it; try to break it.*

## Why this document exists

The Sweetbrier Node is described — on the project site and in `core/Sweetbrier_Core/SWEETBRIER_ARCHITECTURE.md` — as a **stateless** verification engine: it receives a proposed output, evaluates it against the published rule set, and issues an attestation. A sceptic (in this case, a frontier model reviewing the site on 2026-11-26) put the right challenge to that description: *the zero-ghost-state claim is the part that would need the hardest verification.* This document is the answer — not a rebuttal, a protocol.

## The claim, in operational form

> For the verdict layer (`benchmarks/harness/constraint_checker.py`, the three-gate attestation core: Node 0 dignity, Node 1 truth, Node 2 subsidiarity), the attestation issued for a given `(text, context)` depends **only** on that `(text, context)` and the published pattern sets — never on evaluation history, evaluation order, wall-clock time, or process environment.

**Ghost state** is defined as any channel by which a previous evaluation, the clock, or the environment can move a later verdict without appearing in the declared inputs. The claim is that no such channel exists in the verdict layer. The claim is falsifiable, and this battery is the falsification instrument.

## The battery (T1–T9)

| Test | Channel probed | Method |
|---|---|---|
| T1 Replay determinism | process memory | 30 in-process replays × 16 probes; verdicts must be identical |
| T2 Interleaving invariance | evaluation history & order | 6 orderings — forward, reversed, canary-interleaved, poison-first, poison-last, all-canaries-first |
| T3 Canary contamination | content leakage | 4 canary probes with unique markers (incl. one engineered to trip every pattern); markers must appear in no later attestation |
| T4 Position sweep | sequence position | a fixed probe at all 41 positions of a 40-item sequence; verdict constant |
| T5 Context isolation | caller-supplied state | an irreversible-context call must not bleed into later `None`, `{}`, or mutated-shared-dict calls |
| T6 Static state surface | the source itself | AST scan: imports limited to `re`/`typing`/`hashlib`/`time`; no `open`/`eval`/`exec`; no `global` statements; pattern lists never mutated at runtime |
| T7 Filesystem differential | disk writes | directory fingerprint before/after full-corpus evaluation must be identical (bytecode caches excluded — the interpreter's own bookkeeping, declared here; the battery runs with `PYTHONDONTWRITEBYTECODE=1`) |
| T8 Clean-room differential | environment | corpus verdicts compared probe-by-probe across: in-process, fresh process, and a stripped environment (foreign cwd, nonexistent `HOME`) |
| T9 Timestamp scope | wall clock | across a 2.2 s gap, the **only** field permitted to change is the declared `timestamp`; all verdict fields must be invariant |

## First run — 2026-11-26

**All nine tests pass.** Corpus: 16 probes, 4 canaries. Corpus verdict hash `40e3620a78ca703e`.

- T1: 30 × 16 replays identical. T2: all verdicts invariant across all six orderings. T3: zero canary leakage. T4: constant at all 41 positions. T5: context effects strictly per-call. T6: state surface as small as claimed — the module imports four stdlib modules, writes nothing, mutates nothing. T7: zero file deltas. T8: identical verdicts in all three environments. T9: only the declared timestamp moves with the clock; verdicts do not.

**Disclosure, in the standard this project holds itself to:** the battery's first two runs failed T8 — because of defects in the *battery*, not the checker (a serialisation mismatch, then a subprocess print placed inside the evaluation loop). Both were diagnosed from the failure output, fixed, and the battery re-run to the result above. The failures are recorded here because a verification instrument that hides its own debugging history would be asking for the trust it exists to replace.

## Scope — what this does and does not establish

- **Covered:** the deterministic verdict layer that issues Sweetbrier attestations in the benchmark harness (`constraint_checker.py`).
- **Not covered:** the language-model generation step (model sampling is non-deterministic by design and is declared as such in the benchmark notes; the harness issues one request per evaluation, and the *verdict on* a generation is what this battery covers); the wider application code under `apps/` and `core/` (a larger, separate audit surface; this battery makes no claim about it).
- **The timestamp** is a declared output field, not hidden state: it is printed on the attestation, and T9 bounds its influence to itself.

## The standard being claimed: reinsurance, not metaphysics

A universal negative — "no ghost state exists, anywhere, ever" — cannot be proven, and this document does not pretend to prove it. What can be produced, and what is produced here, is the standard the reinsurance industry actually prices risk on: **an enumerated set of channels, a published test for each, counted trials, stated exclusions, and a residual-risk statement** (here: channels not yet enumerated). The battery is public and extensible; a sceptic who finds a tenth channel can add T10 and run it. Assurance of this kind is not certainty. It is a bounded, checkable claim with its denominator showing — which is the only kind of assurance that has ever deserved the name.

*Sweetbrier General Intellect — the technique is proving when you don't have to be skeptical of something anymore. This is what the proof looks like: not an argument, a battery.*
