"""
The Eleven Dimensional Spreadsheet: a tiny proof of concept.

An entry is not real until it is posted on all eleven axes:

   1. debit_account        where the value leaves
   2. credit_account       where the value arrives
   3. forgiveness          the entry's grace standing: "owed" (it creates
                           an obligation), "settled" (complete in itself,
                           or discharging one), or "forgiven" (it releases
                           an obligation without settlement). The third
                           axis of bookkeeping is forgiveness
                           (Christopher's summary, Oct 24, 2026).
   4. amount               how much moved
   5. provenance           the earlier entry this one rests on, or GENESIS
   6. author               who posted it, as a matter of record
   7. reason               why it exists, stated at posting time
   8. consent              every party who agreed, and under what mandate
   9. definition_version   what the words meant on the day it was posted
  10. momentum             where the arrangement is heading: the projected
                           size of the next movement along this chain
                           (Ijiri's dimension)
  11. receipt              one countersigned record, held in common, so
                           neither side keeps a private version that drifts
                           (Grigg's dimension)

  (Every entry also carries posted_at, when it was posted. Time is the
  book's index, the axis the other eleven stand on, not one of them.)

  Axes 1, 2 and 4 are classical double entry. Axes 5 to 9 are the
  testimony dimensions of the higher dimensional bookkeeping plan
  (Oct 23, 2026). Axes 10 and 11 are the deal dimensions of its
  [D:E:A:L] addendum. Axis 3 is the oldest of the new ones: double entry
  could only balance or fail to balance, so nothing in it could ever be
  forgiven, only settled. Adding the third axis is what turns a debt
  machine into a testimony machine.

The checker is the safety property: an entry that is incoherent on ANY axis
has no consistent cell to occupy, and is refused. A lie has to balance on
eleven axes at once, against a chain that must terminate, under definitions
that are pinned, with the consent of everyone it names, carrying a receipt
both sides hold. That is what "trustlessly safe" means here: nobody has to
trust the poster, because the book checks the posting.
"""

import hashlib
import json
from dataclasses import dataclass, field, replace


# ---------------------------------------------------------------- registry

DEFINITIONS = {
    "v1": {
        "share": "a transfer without payment",
        "surplus": "food beyond a site's own need",
    },
    "v2": {
        "share": "a transfer without payment",
        "surplus": "food beyond a site's own need, including projected demand",
    },
}

ACCOUNTS = {  # account -> the party who must consent to movements on it
    "Harvest": "Harvest",
    "NorWest": "NorWest",
    "Siloam": "Siloam",
}


# ------------------------------------------------------------------- entry

@dataclass
class Entry:
    entry_id: str
    debit_account: str          # 1
    credit_account: str         # 2
    amount: float               # 3
    posted_at: str              # 4
    provenance: str             # 5: an earlier entry_id, or "GENESIS"
    author: str                 # 6
    reason: str                 # 7
    consent: tuple              # 8: parties who agreed
    definition_version: str     # 9
    momentum: float = None      # 10: projected size of the next movement
    forgiveness: str = "settled"  # 3: owed / settled / forgiven
    signatures: dict = field(default_factory=dict)  # 11, filled by sign()

    def canonical(self):
        """The ten axes the receipt is computed over."""
        return json.dumps({
            "entry_id": self.entry_id,
            "debit_account": self.debit_account,
            "credit_account": self.credit_account,
            "amount": self.amount,
            "posted_at": self.posted_at,
            "provenance": self.provenance,
            "author": self.author,
            "reason": self.reason,
            "consent": list(self.consent),
            "definition_version": self.definition_version,
            "momentum": self.momentum,
            "forgiveness": self.forgiveness,
        }, sort_keys=True)

    def receipt(self):
        """Axis 11: the record both sides hold in common."""
        return hashlib.sha256(self.canonical().encode()).hexdigest()

    def sign(self, party):
        """A party countersigns by hashing the shared receipt with its name.
        Toy signatures for a proof of concept; the point is the shape: the
        signature is over the COMMON record, so a privately altered copy on
        either side stops verifying."""
        self.signatures[party] = hashlib.sha256(
            (self.receipt() + "|" + party).encode()).hexdigest()
        return self


# ------------------------------------------------------------------- book

class Rejected(Exception):
    pass


class Book:
    def __init__(self):
        self.entries = {}

    # -- the checker: every axis, every time ------------------------------
    def check(self, e):
        if e.entry_id in self.entries:
            raise Rejected("id already posted; the book is append only, "
                           "corrections are new entries, never edits")
        if e.debit_account not in ACCOUNTS or e.credit_account not in ACCOUNTS:
            raise Rejected("unknown account")
        if e.amount <= 0:
            raise Rejected("amount must be positive; forgiveness is an "
                           "axis, not a zero")
        # 3. forgiveness: the grace standing must be one of the three, and
        # a forgiveness entry must actually release a standing obligation:
        # resting on it, reversed against it, for exactly its amount.
        if e.forgiveness not in ("owed", "settled", "forgiven"):
            raise Rejected(f"grace standing '{e.forgiveness}' is not "
                           "owed, settled, or forgiven")
        if e.forgiveness == "forgiven":
            if e.provenance == "GENESIS" or e.provenance not in self.entries:
                raise Rejected("forgiveness must rest on the obligation "
                               "it releases")
            o = self.entries[e.provenance]
            if o.forgiveness != "owed":
                raise Rejected("the entry it rests on is not standing as "
                               "owed; you cannot forgive what was never "
                               "an obligation")
            if (e.debit_account, e.credit_account, e.amount) != \
                    (o.credit_account, o.debit_account, o.amount):
                raise Rejected("forgiveness must reverse the obligation "
                               "exactly; anything else is a new movement "
                               "wearing grace's clothes")
        # 5. provenance: the chain must walk back and TERMINATE.
        if e.provenance == e.entry_id:
            raise Rejected("provenance is the entry itself; a chain that "
                           "rests on itself proves nothing (you cannot "
                           "define a word with itself)")
        seen, cursor = set(), e.provenance
        while cursor != "GENESIS":
            if cursor in seen:
                raise Rejected("provenance chain is cyclic; a chain that "
                               "never reaches a first entry proves nothing "
                               "(you cannot define a word with itself)")
            if cursor not in self.entries:
                raise Rejected(f"provenance '{cursor}' is not in the book; "
                               "the chain dangles")
            seen.add(cursor)
            cursor = self.entries[cursor].provenance
        # 8. consent: everyone the movement touches must have agreed.
        needed = {ACCOUNTS[e.debit_account], ACCOUNTS[e.credit_account]}
        if not needed.issubset(set(e.consent)):
            raise Rejected(f"consent missing: {sorted(needed - set(e.consent))}")
        # 9. definitions are pinned to a registered version.
        if e.definition_version not in DEFINITIONS:
            raise Rejected(f"definition version '{e.definition_version}' "
                           "is not registered; unpinned meanings are how "
                           "ledgers fill with fluent nonsense")
        # 10. momentum: a declared trajectory is checked when the next
        # movement along the chain actually arrives.
        if e.provenance != "GENESIS" and e.forgiveness != "forgiven":
            parent = self.entries[e.provenance]
            if parent.momentum is not None and parent.momentum != e.amount:
                raise Rejected(f"trajectory broken: the parent entry "
                               f"projected a next movement of "
                               f"{parent.momentum}, this entry posts "
                               f"{e.amount}")
        # 11. receipt: both parties hold the SAME record, countersigned.
        for party in needed:
            want = hashlib.sha256(
                (e.receipt() + "|" + party).encode()).hexdigest()
            if e.signatures.get(party) != want:
                raise Rejected(f"receipt does not verify for {party}; one "
                               "side's copy has drifted from the record "
                               "held in common")
        return True

    def post(self, e):
        self.check(e)
        self.entries[e.entry_id] = e
        return e

    # -- reading an old entry under newer meanings -------------------------
    def read(self, entry_id, reader_version):
        e = self.entries[entry_id]
        if reader_version == e.definition_version:
            return f"{entry_id}: read under {reader_version}, the meanings " \
                   f"it was posted under. Clean."
        old = DEFINITIONS[e.definition_version]
        new = DEFINITIONS[reader_version]
        drift = [t for t in old if old[t] != new.get(t)]
        return (f"{entry_id}: WARNING, posted under "
                f"{e.definition_version}, being read under {reader_version}. "
                f"Drifted terms: {drift}. The arithmetic is perfect and "
                f"the reading is wrong; this is why the version is an axis.")

    # -- grace: a reversal that keeps the provenance -----------------------
    def forgive(self, original_id, author, reason, posted_at,
                definition_version):
        """Forgiveness is a possible entry: a reversal, standing 'forgiven'
        on axis 3, that releases a standing obligation while keeping the
        original on the record. The undo that does not lie. The checker
        enforces the shape; this helper is just the convenient pen."""
        o = self.entries[original_id]
        e = Entry(
            entry_id=original_id + "-forgiven",
            debit_account=o.credit_account,
            credit_account=o.debit_account,
            amount=o.amount,
            posted_at=posted_at,
            provenance=original_id,
            author=author,
            reason=reason,
            consent=tuple(sorted({ACCOUNTS[o.debit_account],
                                  ACCOUNTS[o.credit_account]})),
            definition_version=definition_version,
            momentum=None,
            forgiveness="forgiven",
        )
        e.sign(ACCOUNTS[o.debit_account]).sign(ACCOUNTS[o.credit_account])
        return self.post(e)
