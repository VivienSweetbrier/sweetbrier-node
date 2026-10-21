#!/usr/bin/env python3
"""
OBB CORE PRIMITIVES — LOCAL STATE & PROVENANCE UTILITY
License: GNU AGPLv3
Attestation: probabilistic_structural

Provides three self-contained, general-purpose local software utilities:
1. ObbSafetyFloor: Zero-PII payload validation and sanitization.
2. ObbLibraryLedger: Deterministic SHA-256 hash-chained provenance log.
3. ObbUndoEngine: Immutable state snapshots with 1-step atomic rollback.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, FrozenSet, List, Optional


def canonical_sha256(data: Any) -> str:
    """Compute a deterministic SHA-256 hex digest over any JSON-serializable structure."""
    encoded = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class ObbSafetyFloor:
    """
    Enforces a strict Zero-PII local safety floor before any state is logged or snapshotted.
    """

    DEFAULT_FORBIDDEN_KEYS: FrozenSet[str] = frozenset(
        {
            "ssn",
            "social_security",
            "sin",
            "passport",
            "password",
            "secret_key",
            "private_key",
            "credit_card",
            "card_number",
            "email",
            "phone",
            "phone_number",
            "home_address",
            "date_of_birth",
            "dob",
        }
    )

    def __init__(self, extra_forbidden_keys: Optional[FrozenSet[str]] = None) -> None:
        self.forbidden_keys = self.DEFAULT_FORBIDDEN_KEYS | (extra_forbidden_keys or frozenset())

    def scan_violations(self, payload: Any, path: str = "root") -> List[str]:
        """Recursively scan a nested dict/list structure for forbidden PII keys."""
        violations: List[str] = []
        if isinstance(payload, dict):
            for k, v in payload.items():
                normalized = str(k).strip().lower()
                current_path = f"{path}.{k}"
                if normalized in self.forbidden_keys:
                    violations.append(current_path)
                violations.extend(self.scan_violations(v, current_path))
        elif isinstance(payload, list):
            for idx, item in enumerate(payload):
                violations.extend(self.scan_violations(item, f"{path}[{idx}]"))
        return violations

    def assert_clean(self, payload: Any) -> None:
        """Raise ValueError if any forbidden PII key is present in the payload."""
        violations = self.scan_violations(payload)
        if violations:
            raise ValueError(f"ObbSafetyFloor violation: forbidden PII fields detected at {violations}")


@dataclass(frozen=True)
class LedgerEntry:
    sequence: int
    timestamp_utc: str
    action_label: str
    parent_hash: str
    payload_hash: str
    entry_hash: str
    attestation: str = "probabilistic_structural"


class ObbLibraryLedger:
    """
    Append-only, hash-chained provenance ledger for local state transitions.
    """

    GENESIS_HASH = "0" * 64

    def __init__(self, safety_floor: Optional[ObbSafetyFloor] = None) -> None:
        self.safety_floor = safety_floor or ObbSafetyFloor()
        self._entries: List[LedgerEntry] = []

    @property
    def entries(self) -> List[LedgerEntry]:
        return list(self._entries)

    @property
    def head_hash(self) -> str:
        return self._entries[-1].entry_hash if self._entries else self.GENESIS_HASH

    def append(self, action_label: str, payload: Dict[str, Any]) -> LedgerEntry:
        self.safety_floor.assert_clean(payload)
        seq = len(self._entries) + 1
        now_utc = datetime.now(timezone.utc).isoformat()
        parent = self.head_hash
        p_hash = canonical_sha256(payload)
        e_hash = canonical_sha256(
            {
                "sequence": seq,
                "timestamp_utc": now_utc,
                "action_label": action_label,
                "parent_hash": parent,
                "payload_hash": p_hash,
            }
        )
        entry = LedgerEntry(
            sequence=seq,
            timestamp_utc=now_utc,
            action_label=action_label,
            parent_hash=parent,
            payload_hash=p_hash,
            entry_hash=e_hash,
        )
        self._entries.append(entry)
        return entry

    def verify_chain(self) -> bool:
        """Verify that every entry in the ledger links cleanly to its parent hash."""
        expected_parent = self.GENESIS_HASH
        for entry in self._entries:
            if entry.parent_hash != expected_parent:
                return False
            recomputed = canonical_sha256(
                {
                    "sequence": entry.sequence,
                    "timestamp_utc": entry.timestamp_utc,
                    "action_label": entry.action_label,
                    "parent_hash": entry.parent_hash,
                    "payload_hash": entry.payload_hash,
                }
            )
            if recomputed != entry.entry_hash:
                return False
            expected_parent = entry.entry_hash
        return True


@dataclass(frozen=True)
class StateSnapshot:
    snapshot_id: str
    state_hash: str
    ledger_head_hash: str
    timestamp_utc: str
    state_copy: Dict[str, Any]


class ObbUndoEngine:
    """
    Manages immutable state snapshots and provides 1-step atomic rollback
    with cryptographic integrity verification.
    """

    def __init__(
        self,
        initial_state: Optional[Dict[str, Any]] = None,
        ledger: Optional[ObbLibraryLedger] = None,
    ) -> None:
        self.ledger = ledger or ObbLibraryLedger()
        self._snapshots: Dict[str, StateSnapshot] = {}
        self._history_order: List[str] = []
        self._current_state: Dict[str, Any] = {}
        if initial_state is not None:
            self.commit("INITIAL_STATE", initial_state)

    @property
    def current_state(self) -> Dict[str, Any]:
        return copy.deepcopy(self._current_state)

    def commit(self, label: str, new_state: Dict[str, Any]) -> StateSnapshot:
        """Validate, log, and snapshot a new state."""
        entry = self.ledger.append(label, new_state)
        frozen_copy = copy.deepcopy(new_state)
        s_hash = canonical_sha256(frozen_copy)
        snap_id = f"SNAP-{entry.sequence:04d}-{s_hash[:10].upper()}"
        snapshot = StateSnapshot(
            snapshot_id=snap_id,
            state_hash=s_hash,
            ledger_head_hash=entry.entry_hash,
            timestamp_utc=entry.timestamp_utc,
            state_copy=frozen_copy,
        )
        self._snapshots[snap_id] = snapshot
        self._history_order.append(snap_id)
        self._current_state = copy.deepcopy(frozen_copy)
        return snapshot

    def undo(self, target_snapshot_id: Optional[str] = None) -> StateSnapshot:
        """
        Atomically restore state to a specific snapshot ID (or the immediately previous snapshot).
        Verifies snapshot hash integrity prior to restoration.
        """
        if not self._history_order:
            raise RuntimeError("No snapshots available to undo.")

        if target_snapshot_id is None:
            if len(self._history_order) < 2:
                raise RuntimeError("Already at the earliest snapshot; cannot undo further.")
            target_snapshot_id = self._history_order[-2]

        if target_snapshot_id not in self._snapshots:
            raise KeyError(f"Snapshot '{target_snapshot_id}' not found.")

        snapshot = self._snapshots[target_snapshot_id]
        actual_hash = canonical_sha256(snapshot.state_copy)
        if actual_hash != snapshot.state_hash:
            raise ValueError(f"Snapshot integrity check failed for {target_snapshot_id}")

        self.ledger.append(f"ATOMIC_UNDO_TO:{target_snapshot_id}", snapshot.state_copy)
        self._current_state = copy.deepcopy(snapshot.state_copy)
        return snapshot


if __name__ == "__main__":
    engine = ObbUndoEngine({"project": "local_sandbox", "balance": 1000, "status": "clean"})
    snap1 = engine._history_order[-1]

    snap2 = engine.commit("ALLOCATE_EQUIPMENT", {"project": "local_sandbox", "balance": 400, "status": "allocated"})
    restored = engine.undo(snap1)

    # Verify PII rejection works cleanly
    pii_blocked = False
    try:
        engine.commit("BAD_COMMIT", {"project": "local_sandbox", "email": "user@example.com"})
    except ValueError:
        pii_blocked = True

    summary = {
        "attestation": "probabilistic_structural",
        "initial_snapshot": snap1,
        "second_snapshot": snap2.snapshot_id,
        "restored_state": engine.current_state,
        "ledger_entries_count": len(engine.ledger.entries),
        "ledger_chain_valid": engine.ledger.verify_chain(),
        "safety_floor_blocked_pii": pii_blocked,
    }
    print(json.dumps(summary, indent=2))
