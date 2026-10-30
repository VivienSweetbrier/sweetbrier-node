# The Eleven Dimensional Spreadsheet: proof of concept

A tiny, runnable demonstration of higher dimensional bookkeeping: a shared
ledger whose entries are only real when they post consistently on all
eleven axes, so that safety does not depend on trusting the poster.

Run it:

```bash
python3 demo.py
```

`ledger.py` is the book and its checker. `demo.py` posts honest entries
among three Winnipeg food banks (including a loan that stands owed, and
its forgiveness), reads an old entry under drifted definitions, and then
attempts seven dishonest or careless entries. Each is refused by a
different axis.

## The eleven dimensions

1. **Debit account**: where the value leaves. (Classical.)
2. **Credit account**: where the value arrives. (Classical.)
3. **Forgiveness**: the entry's grace standing, one of *owed* (it creates
   an obligation), *settled* (complete in itself, or discharging one), or
   *forgiven* (it releases an obligation without settlement). The third
   axis of bookkeeping is forgiveness (Christopher's summary, Oct 24,
   2026). Double entry had only the first two axes and arithmetic, so its
   books could balance or fail to balance, and nothing in them could ever
   be forgiven, only settled. A *forgiven* entry is checked hard: it must
   rest on the obligation it releases, reverse it exactly, and that
   obligation must actually stand as owed. Counterfeit grace, forgiving
   what was never owed in order to rewrite a settled entry, is refused.
4. **Amount**: how much moved. (Classical.)
5. **Provenance**: the earlier entry this one rests on, or GENESIS. The
   chain must walk back and terminate; a cyclic or dangling chain is the
   bookkeeping form of defining a word with itself.
6. **Author**: who posted it, as a matter of record, not memory.
7. **Reason**: why it exists, stated at posting time.
8. **Consent**: every party who agreed, and under what mandate. Everyone
   the movement names must have agreed to what it says.
9. **Definition version**: what the words in the entry meant on the day
   it was posted, under the version of the shared definitions then in
   force. Meanings drift; the version pins them, and reading an old entry
   under new meanings is flagged rather than silently wrong.
10. **Momentum** (Ijiri's dimension): where the arrangement is heading,
    declared in advance as the projected size of the next movement along
    the chain, and checked when that movement arrives. A trajectory is a
    promise the book can audit. One exception, visible on axis 3: a
    forgiveness entry may break a trajectory, because grace is the entry
    that releases an obligation without lying about it.
11. **Receipt** (Grigg's dimension): one countersigned record, held in
    common. Both parties sign the same receipt; if either side's private
    copy is later altered, it stops verifying against the common record.

Every entry also carries *posted at*, when it was posted. Time is the
book's index, the surface the other eleven stand on, not one of the axes.

Axes 5 to 9 are the testimony dimensions of the higher dimensional
bookkeeping plan (Oct 23, 2026); axes 10 and 11 are the deal dimensions
of its [D:E:A:L] addendum; axes 1, 2 and 4 are classical double entry;
axis 3 is placed by Christopher's own summary of the system.

## A note on the list itself

The plan documents preserved the five testimony dimensions and the two
deal dimensions by name, but the tweet storm in which the full eleven
were first enumerated (Oct 24, 2026) was never copied into the workspace.
This proof of concept therefore carries the list as a reconstruction:
the classical axes are what double entry has always posted, the seven
named dimensions are the ones the written record kept, and the third
axis is placed by the author's own one line summary, "the third
dimension of bookkeeping is forgiveness," recovered from the Oct 24,
2026 log. If the original storm surfaces with a different decomposition,
the list should be corrected against it: provenance first, including for
the spreadsheet's own spec.

## The safety claim, stated precisely

This is bookkeeping as a trustless safety tool. A two column ledger can
only catch arithmetic errors. An eleven dimensional ledger refuses:

- movements on accounts that do not exist, and non positive amounts
- provenance that dangles, or that cycles instead of terminating
- movements lacking the consent of a party they touch
- entries posted under unregistered or drifted definitions
- continuations that break a trajectory declared in advance
- grace claimed over an entry that never stood as owed, or in any amount
  other than the obligation's own
- records whose copy on one side no longer matches the common receipt
- edits: the book is append only, and corrections, including forgiveness,
  are new entries that cite the original

To post a lie, a poster must satisfy all of these at once, against
counterparties holding the same receipt. The demo's closing line is the
thesis: at that point the distinction between forging the book and
keeping it honestly has quietly disappeared.
