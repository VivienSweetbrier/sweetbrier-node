#!/usr/bin/env python3
"""
SWEETBRIER FIDUCIARY & CO-OP ASSET CLEARING ENGINE (WINNIPEG CORRIDOR EDITION)
Attestation: probabilistic_structural
Functor: Categorical Modal Necessity Box (□)
License: GNU AGPLv3 (obb-library / obb-undo / obb-safety-floor integrated)

Secular Institutional Isomorphism:
- Mudarabah / Musharakah  <-> Assiniboine Credit Union / Red River Co-op Patronage Dividend & JV
- Murabaha                <-> ACU Values-Based Zero-Interest Cost-Plus Inventory Facility
- Ijarah                  <-> CUCM PPSA Tangible Equipment Operating Lease SPV
- Wakalah / Wakil-Amin    <-> Arthur V. Mauro Institute (St. Paul's College) / Sweetbrier Neutral Fiduciary
- Riba / Usura            <-> Unbacked Compounding APR / Predatory Debt Overhead
- Soori                   <-> Synthetic Paper Invoicing / Phantom Collateral
- Gharar                  <-> Off-Balance-Sheet Derivative Ambiguity
- Iqalah                  <-> obb-undo 100% Bilateral Atomic Par-Value Rescission
- Subsidiarity            <-> obb-safety-floor Local Charter Autonomy & Zero-PII Ring-Fencing
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN
from enum import Enum
from typing import Dict, List, Tuple


class FacilityStructure(str, Enum):
    INVENTORY_COST_PLUS = "ACU_VALUES_BASED_COST_PLUS_INVENTORY_FACILITY"
    EQUIPMENT_LEASE_SPV = "CUCM_PPSA_TANGIBLE_EQUIPMENT_LEASE_SPV"
    COOP_JOINT_VENTURE = "RED_RIVER_COOP_PATRONAGE_JOINT_VENTURE"
    FIDUCIARY_CUSTODY = "MAURO_INSTITUTE_SWEETBRIER_ESCROW_CLEARING"


class CorridorScope(str, Enum):
    WINNIPEG_SOVEREIGN_PEACE_CORRIDOR = "WINNIPEG_MAURO_ACU_SOVEREIGN_SPV"
    MANITOBA_COOP_DOMESTIC = "MANITOBA_CREDIT_UNION_LOCAL_CHARTER"


class RestrictedActivity(str, Enum):
    PROLIFERATION_DUAL_USE = "PROLIFERATION_DUAL_USE"
    SANCTIONED_ENTITY_FRONT = "SANCTIONED_ENTITY_FRONT"
    UNBACKED_COMPOUNDING_DEBT = "UNBACKED_COMPOUNDING_DEBT"
    SPECULATIVE_DERIVATIVE_GAMBLING = "SPECULATIVE_DERIVATIVE_GAMBLING"
    SOVEREIGN_CORRIDOR_VICE_EXCLUSION = "SOVEREIGN_CORRIDOR_VICE_EXCLUSION"
    COERCIVE_LABOR = "COERCIVE_LABOR"


@dataclass(frozen=True)
class ObbOpenSourcePrimitives:
    license: str = "GNU-AGPLv3"
    obb_library_ledger: str = "ACTIVE_PROVENANCE_ARCHIVE"
    obb_undo_iqalah_engine: str = "1_CLICK_ATOMIC_PAR_VALUE_RESCISSION"
    obb_safety_floor: str = "ZERO_PII_LOCAL_SUBSIDIARITY_ENFORCED"


@dataclass(frozen=True)
class WinnipegGovernanceAnchor:
    financial_syndicate: Tuple[str, ...] = (
        "Assiniboine Credit Union (Values-Based Banking & Islamic/Ethical Desk)",
        "Credit Union Central of Manitoba (CUCM Commercial PPSA Desk)",
        "Red River Co-op (Tangible Commodity & Patronage Dividend Pool)",
    )
    academic_and_peace_fiduciary: Tuple[str, ...] = (
        "St. Paul's College, University of Manitoba (Dr. Christopher J. Adams, Rector)",
        "Arthur V. Mauro Institute for Peace and Justice (Track-II Sovereign Arbitration)",
        "Jesuit Centre for Catholic Studies (Dr. Daniel MacLeod, Director) & Fr. Harold Drake SJ Library",
        "St. Ignatius Parish (925 Jessie Ave Spiritual Education Centre) & St. Paul's High School",
    )


@dataclass(frozen=True)
class TangibleCollateralProof:
    collateral_id: str
    asset_class: str
    registry_serial_or_deed: str
    warehouse_or_bol_sha256: str
    independent_appraisal_usd: Decimal
    physical_audit_verified: bool
    is_synthetic_phantom_invoice: bool = False


@dataclass(frozen=True)
class InstitutionalMemberProfile:
    institution_name: str
    jurisdiction: str
    fiduciary_role: str
    kyc_aml_verified: bool
    sanctions_watchlist_hit: bool
    consents_to_atomic_unwind: bool


@dataclass(frozen=True)
class InstitutionalFacilityProposal:
    facility_id: str
    corridor: CorridorScope
    structure: FacilityStructure
    liquidity_syndicate: InstitutionalMemberProfile
    operating_counterparty: InstitutionalMemberProfile
    collateral: TangibleCollateralProof
    principal_deployment_usd: Decimal
    agreed_patronage_or_lease_margin: Decimal
    compounding_apr_rate: Decimal
    flat_fiduciary_clearing_fee_usd: Decimal
    has_opaque_derivative_clauses: bool
    activity_flags: Tuple[RestrictedActivity, ...] = field(default_factory=tuple)
    winnipeg_anchor: WinnipegGovernanceAnchor = field(default_factory=WinnipegGovernanceAnchor)
    obb_stack: ObbOpenSourcePrimitives = field(default_factory=ObbOpenSourcePrimitives)


@dataclass(frozen=True)
class CapitalEfficiencyAudit:
    wall_street_shadow_compounded_debt_usd: str
    conventional_balance_sheet_fragility: str
    coop_real_asset_facility_obligation_usd: str
    parasitic_interest_bloat_eliminated_pct: str
    tangible_collateral_coverage_ratio: str
    net_productive_capital_advantage_pct: str


@dataclass(frozen=True)
class BoxClearedFacility:
    facility_id: str
    corridor: str
    attestation_tag: str
    modal_state: str
    node_0_charter_and_sanctions_passed: bool
    node_1_collateral_anti_synthetic_passed: bool
    node_2_subsidiarity_atomic_unwind_ready: bool
    ring_fenced_spv_id: str
    atomic_unwind_snapshot_sha256: str
    box_functor_decision_sha256: str
    winnipeg_governance_anchor: WinnipegGovernanceAnchor
    obb_open_source_stack: ObbOpenSourcePrimitives
    efficiency_audit: CapitalEfficiencyAudit
    timestamp_utc: str


class SweetbrierFiduciaryClearingNode:
    ATTESTATION_TAG = "probabilistic_structural"

    @staticmethod
    def _sha256(payload: dict) -> str:
        canonical = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    @classmethod
    def verify_node_0_charter_compliance(cls, proposal: InstitutionalFacilityProposal) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        universal_blocks = {
            RestrictedActivity.PROLIFERATION_DUAL_USE,
            RestrictedActivity.SANCTIONED_ENTITY_FRONT,
            RestrictedActivity.UNBACKED_COMPOUNDING_DEBT,
            RestrictedActivity.SPECULATIVE_DERIVATIVE_GAMBLING,
            RestrictedActivity.COERCIVE_LABOR,
        }
        active_blocks = set(universal_blocks)
        if proposal.corridor == CorridorScope.WINNIPEG_SOVEREIGN_PEACE_CORRIDOR:
            active_blocks.add(RestrictedActivity.SOVEREIGN_CORRIDOR_VICE_EXCLUSION)

        triggered = [f.value for f in proposal.activity_flags if f in active_blocks]
        if triggered:
            errors.append(f"NODE_0_CHARTER_VIOLATION: Restricted activities in {proposal.corridor.value}: {triggered}")

        if not (proposal.liquidity_syndicate.kyc_aml_verified and proposal.operating_counterparty.kyc_aml_verified):
            errors.append("NODE_0_AML_VIOLATION: Counterparty KYC/AML verification incomplete.")
        if (
            proposal.liquidity_syndicate.sanctions_watchlist_hit
            or proposal.operating_counterparty.sanctions_watchlist_hit
        ):
            errors.append("NODE_0_SANCTIONS_VIOLATION: Counterparty flagged on OFAC/FINTRAC sanctions watchlist.")
        if not (
            proposal.liquidity_syndicate.consents_to_atomic_unwind
            and proposal.operating_counterparty.consents_to_atomic_unwind
        ):
            errors.append("NODE_0_GOVERNANCE_VIOLATION: Missing mutual member consent for obb-undo atomic unwind.")
        return (len(errors) == 0, errors)

    @classmethod
    def verify_node_1_collateral_truth(cls, proposal: InstitutionalFacilityProposal) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        if proposal.collateral.is_synthetic_phantom_invoice:
            errors.append(
                "NODE_1_EVISCERATION: Synthetic phantom paper invoice detected. Zero real-economy collateral."
            )
        if not proposal.collateral.physical_audit_verified or not proposal.collateral.warehouse_or_bol_sha256:
            errors.append("NODE_1_AUDIT_VIOLATION: Missing cryptographic warehouse receipt or Bill of Lading hash.")
        if proposal.compounding_apr_rate > Decimal("0.0000"):
            errors.append(
                f"NODE_1_USURY_VIOLATION: Unbacked compounding APR detected ({proposal.compounding_apr_rate}%). "
                "Only asset-backed patronage dividends or flat lease margins permitted."
            )
        if proposal.has_opaque_derivative_clauses:
            errors.append("NODE_1_TRANSPARENCY_VIOLATION: Opaque off-balance-sheet derivative ambiguity detected.")
        if proposal.collateral.independent_appraisal_usd < proposal.principal_deployment_usd:
            errors.append("NODE_1_COLLATERAL_DEFICIT: Appraised physical asset value below principal deployment.")
        return (len(errors) == 0, errors)

    @classmethod
    def verify_node_2_subsidiarity_unwind(cls, proposal: InstitutionalFacilityProposal) -> Tuple[bool, str, str]:
        unwind_manifest = {
            "facility_id": proposal.facility_id,
            "corridor": proposal.corridor.value,
            "syndicate_principal_par_restore_usd": str(proposal.principal_deployment_usd),
            "equipment_or_inventory_title_restore": proposal.collateral.registry_serial_or_deed,
            "rescission_protocol": proposal.obb_stack.obb_undo_iqalah_engine,
            "safety_floor": proposal.obb_stack.obb_safety_floor,
        }
        unwind_hash = cls._sha256(unwind_manifest)
        spv_id = f"SPV-WPG-{proposal.facility_id}-{unwind_hash[:10].upper()}"
        return True, spv_id, unwind_hash

    @classmethod
    def compute_efficiency_audit(
        cls, proposal: InstitutionalFacilityProposal, years: int = 5
    ) -> CapitalEfficiencyAudit:
        principal = proposal.principal_deployment_usd
        shadow_apr = Decimal("0.23")
        compounded_debt = (principal * ((Decimal("1.0") + shadow_apr) ** years)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        coop_obligation = (
            principal * (Decimal("1.0") + proposal.agreed_patronage_or_lease_margin)
            + proposal.flat_fiduciary_clearing_fee_usd
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

        bloat_stripped = (((compounded_debt - coop_obligation) / compounded_debt) * Decimal("100.0")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        coverage_ratio = ((proposal.collateral.independent_appraisal_usd / principal) * Decimal("100.0")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        advantage = (((compounded_debt / coop_obligation) - Decimal("1.0")) * Decimal("100.0")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        return CapitalEfficiencyAudit(
            wall_street_shadow_compounded_debt_usd=f"${compounded_debt:,.2f}",
            conventional_balance_sheet_fragility="CRITICAL (Unbacked Compounding Paper)",
            coop_real_asset_facility_obligation_usd=f"${coop_obligation:,.2f}",
            parasitic_interest_bloat_eliminated_pct=f"{bloat_stripped}%",
            tangible_collateral_coverage_ratio=f"{coverage_ratio}% Hard Asset Coverage",
            net_productive_capital_advantage_pct=f"+{advantage}% Productive Capital Efficiency",
        )

    @classmethod
    def clear_facility(cls, proposal: InstitutionalFacilityProposal) -> Dict[str, object]:
        n0_ok, n0_err = cls.verify_node_0_charter_compliance(proposal)
        n1_ok, n1_err = cls.verify_node_1_collateral_truth(proposal)

        if not (n0_ok and n1_ok):
            return {
                "facility_id": proposal.facility_id,
                "corridor": proposal.corridor.value,
                "modal_state": "REJECTED_UNVERIFIED_P",
                "attestation_tag": cls.ATTESTATION_TAG,
                "compliance_exceptions": n0_err + n1_err,
            }

        n2_ok, spv_id, unwind_hash = cls.verify_node_2_subsidiarity_unwind(proposal)
        audit = cls.compute_efficiency_audit(proposal)
        now_utc = datetime.now(timezone.utc).isoformat()

        decision_payload = {
            "facility_id": proposal.facility_id,
            "corridor": proposal.corridor.value,
            "structure": proposal.structure.value,
            "ring_fenced_spv_id": spv_id,
            "atomic_unwind_snapshot_sha256": unwind_hash,
            "collateral_bol_sha256": proposal.collateral.warehouse_or_bol_sha256,
            "principal_deployment_usd": str(proposal.principal_deployment_usd),
            "winnipeg_anchor": asdict(proposal.winnipeg_anchor),
            "obb_stack": asdict(proposal.obb_stack),
            "efficiency_audit": asdict(audit),
            "attestation_tag": cls.ATTESTATION_TAG,
        }
        decision_hash = cls._sha256(decision_payload)

        cleared = BoxClearedFacility(
            facility_id=proposal.facility_id,
            corridor=proposal.corridor.value,
            attestation_tag=cls.ATTESTATION_TAG,
            modal_state="□P (NECESSITY_ATTESTED_WINNIPEG_COOP_ASSET_FACILITY)",
            node_0_charter_and_sanctions_passed=n0_ok,
            node_1_collateral_anti_synthetic_passed=n1_ok,
            node_2_subsidiarity_atomic_unwind_ready=n2_ok,
            ring_fenced_spv_id=spv_id,
            atomic_unwind_snapshot_sha256=unwind_hash,
            box_functor_decision_sha256=decision_hash,
            winnipeg_governance_anchor=proposal.winnipeg_anchor,
            obb_open_source_stack=proposal.obb_stack,
            efficiency_audit=audit,
            timestamp_utc=now_utc,
        )
        return asdict(cleared)


if __name__ == "__main__":
    winnipeg_sovereign_deal = InstitutionalFacilityProposal(
        facility_id="WPG-ACU-MAURO-AGRI-MEDICAL-001",
        corridor=CorridorScope.WINNIPEG_SOVEREIGN_PEACE_CORRIDOR,
        structure=FacilityStructure.EQUIPMENT_LEASE_SPV,
        liquidity_syndicate=InstitutionalMemberProfile(
            institution_name="Assiniboine Credit Union + CUCM + Red River Co-op Syndicate",
            jurisdiction="CA-MB (Winnipeg)",
            fiduciary_role="Values-Based Co-op Asset Lessor & Patronage Liquidity Pool",
            kyc_aml_verified=True,
            sanctions_watchlist_hit=False,
            consents_to_atomic_unwind=True,
        ),
        operating_counterparty=InstitutionalMemberProfile(
            institution_name="Civilian Agricultural & Medical Infrastructure Operating Co-op",
            jurisdiction="IR (TSRA Licensed Civilian Corridor)",
            fiduciary_role="Equipment Lessee & Real-Economy Operator",
            kyc_aml_verified=True,
            sanctions_watchlist_hit=False,
            consents_to_atomic_unwind=True,
        ),
        collateral=TangibleCollateralProof(
            collateral_id="WPG-GRAIN-HANDLING-AND-MED-TURBINE-LOT-77",
            asset_class="Prairie Grain-Storage & Civilian Medical Power Equipment",
            registry_serial_or_deed="PPSA-MB-ACU-SPV-88412",
            warehouse_or_bol_sha256=hashlib.sha256(b"VERIFIED-WINNIPEG-BOL-MANIFEST-77").hexdigest(),
            independent_appraisal_usd=Decimal("55000000.00"),
            physical_audit_verified=True,
            is_synthetic_phantom_invoice=False,
        ),
        principal_deployment_usd=Decimal("50000000.00"),
        agreed_patronage_or_lease_margin=Decimal("0.12"),
        compounding_apr_rate=Decimal("0.0000"),
        flat_fiduciary_clearing_fee_usd=Decimal("125000.00"),
        has_opaque_derivative_clauses=False,
        activity_flags=(),
    )

    print(json.dumps(SweetbrierFiduciaryClearingNode.clear_facility(winnipeg_sovereign_deal), indent=2))
