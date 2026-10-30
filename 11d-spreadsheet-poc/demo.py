"""
Demo: three food banks share surplus on an eleven dimensional book.

Run:  python3 demo.py

Watch for the pattern: honest entries post, including one that stands
OWED and one that forgives it. Every dishonest or careless entry is
refused, each time by a DIFFERENT axis. That spread is the point.
A two column ledger can only catch bad arithmetic. An eleven dimensional
one catches bad provenance, missing consent, drifted meanings, broken
trajectories, private copies, and counterfeit grace, because a lie has
to be consistent on every axis at once, and consistency on eleven axes
against a terminating chain is indistinguishable from the truth.
"""

from ledger import Book, Entry, Rejected


def attempt(book, entry, note):
    try:
        book.post(entry)
        print(f"  POSTED   {entry.entry_id:<16} {note}")
    except Rejected as r:
        print(f"  REFUSED  {entry.entry_id:<16} {note}\n"
              f"           -> {r}")


def signed(e, *parties):
    for p in parties:
        e.sign(p)
    return e


book = Book()

print("Honest entries:")
e1 = signed(Entry(
    entry_id="E1", debit_account="Harvest", credit_account="NorWest",
    amount=40, posted_at="2026-10-30T09:00", provenance="GENESIS",
    author="Harvest coordinator", reason="weekly surplus share",
    consent=("Harvest", "NorWest"), definition_version="v1",
    momentum=40, forgiveness="settled"), "Harvest", "NorWest")
attempt(book, e1, "Harvest sends NorWest 40 crates; projects 40 onward")

e2 = signed(Entry(
    entry_id="E2", debit_account="NorWest", credit_account="Siloam",
    amount=40, posted_at="2026-10-30T11:00", provenance="E1",
    author="NorWest driver", reason="onward share, same surplus",
    consent=("NorWest", "Siloam"), definition_version="v1",
    momentum=None, forgiveness="settled"), "NorWest", "Siloam")
attempt(book, e2, "NorWest passes the 40 to Siloam, as projected")

e3 = signed(Entry(
    entry_id="E3", debit_account="Harvest", credit_account="Siloam",
    amount=10, posted_at="2026-10-30T12:00", provenance="E2",
    author="Harvest coordinator",
    reason="crates lent against next week's delivery",
    consent=("Harvest", "Siloam"), definition_version="v1",
    momentum=None, forgiveness="owed"), "Harvest", "Siloam")
attempt(book, e3, "Harvest lends Siloam 10 crates; the entry stands OWED "
                  "on axis 3")

print("\nReading old entries under new definitions:")
print(" ", book.read("E1", "v1"))
print(" ", book.read("E1", "v2"))

print("\nGrace:")
book.forgive("E3", author="Harvest coordinator",
             reason="the loan is released; Siloam keeps the crates, "
                    "Harvest keeps the record",
             posted_at="2026-10-30T13:00", definition_version="v1")
print("  POSTED   E3-forgiven      axis 3 flips owed -> forgiven by a "
      "reversal entry;\n           E3 itself remains on the record, "
      "unsettled and unhidden")

print("\nDishonest and careless entries:")
b1 = signed(Entry(
    entry_id="B1", debit_account="Harvest", credit_account="NorWest",
    amount=15, posted_at="2026-10-30T14:00", provenance="E1",
    author="Harvest coordinator", reason="quiet extra share",
    consent=("Harvest",), definition_version="v1",
    momentum=None), "Harvest", "NorWest")
attempt(book, b1, "only one side agreed to this one")

b2 = signed(Entry(
    entry_id="B2", debit_account="Harvest", credit_account="Siloam",
    amount=10, posted_at="2026-10-30T14:05", provenance="E99",
    author="unknown", reason="rests on an entry nobody can find",
    consent=("Harvest", "Siloam"), definition_version="v1",
    momentum=None), "Harvest", "Siloam")
attempt(book, b2, "provenance points outside the book")

b2b = signed(Entry(
    entry_id="B2b", debit_account="Harvest", credit_account="Siloam",
    amount=10, posted_at="2026-10-30T14:06", provenance="B2b",
    author="unknown", reason="rests on itself",
    consent=("Harvest", "Siloam"), definition_version="v1",
    momentum=None), "Harvest", "Siloam")
attempt(book, b2b, "provenance is itself: a cyclic definition")

b3 = signed(Entry(
    entry_id="B3", debit_account="NorWest", credit_account="Siloam",
    amount=5, posted_at="2026-10-30T14:10", provenance="E2",
    author="NorWest driver", reason="top up",
    consent=("NorWest", "Siloam"), definition_version="v9",
    momentum=None), "NorWest", "Siloam")
attempt(book, b3, "posted under meanings that were never registered")

b4 = signed(Entry(
    entry_id="B4", debit_account="Harvest", credit_account="NorWest",
    amount=40, posted_at="2026-10-30T14:15", provenance="E2",
    author="Harvest coordinator", reason="second share",
    consent=("Harvest", "NorWest"), definition_version="v1",
    momentum=None), "Harvest", "NorWest")
b4.amount = 400  # one side quietly edits its copy after signing
attempt(book, b4, "the amount grew after both sides signed")

b5 = signed(Entry(
    entry_id="B5", debit_account="NorWest", credit_account="Siloam",
    amount=25, posted_at="2026-10-30T14:20", provenance="E1",
    author="NorWest driver", reason="onward share, smaller than projected",
    consent=("NorWest", "Siloam"), definition_version="v1",
    momentum=None), "NorWest", "Siloam")
attempt(book, b5, "the chain projected 40 onward; this posts 25")

b6 = signed(Entry(
    entry_id="B6", debit_account="NorWest", credit_account="Harvest",
    amount=40, posted_at="2026-10-30T14:25", provenance="E1",
    author="NorWest driver", reason="forgiving the share, retroactively",
    consent=("NorWest", "Harvest"), definition_version="v1",
    momentum=None, forgiveness="forgiven"), "NorWest", "Harvest")
attempt(book, b6, "claims to forgive E1, which never stood as owed: "
                  "grace as a costume for rewriting a settled entry")

print(f"\nThe book holds {len(book.entries)} entries. "
      "Every refusal above names its axis.")
print("Safety property: to post a lie here, you must forge a terminating "
      "provenance chain,\ncollect the consent of everyone it names, pin "
      "meanings that were never in force,\nmatch a trajectory declared in "
      "advance, and hold a receipt identical to your\ncounterparty's. At "
      "that point the distinction between forging the book and keeping\n"
      "it honestly has quietly disappeared.")
