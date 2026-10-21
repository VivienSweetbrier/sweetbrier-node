import json
import uuid
import networkx as nx
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Set, FrozenSet

@dataclass(frozen=True)
class EvaluationState:
    status: str = "APPROVED"
    kinship_cost: float = 1.0
    actions: Tuple[Dict[str, Any], ...] = ()

class PureSweetbrierEngine:
    def __init__(self, master_state: Dict[str, Any]):
        # Immutable reference state
        self.master_graph = nx.DiGraph()
        self.master_graph.add_nodes_from(master_state["nodes"])
        self.master_graph.add_edges_from(master_state.get("edges", []))
        self.mutually_exclusive: Set[FrozenSet[str]] = set(master_state["mutually_exclusive"])
        self.higher_order_principles: Dict[FrozenSet[str], Dict[str, str]] = master_state["higher_order_principles"]

    def _cliometric_filter(self, state: EvaluationState, local_dag: Dict[str, Any]) -> Tuple[bool, EvaluationState, str]:
        if "UNSAFE_MARKET" in local_dag.get("nodes", []):
            return False, state, "Proposal statistically leads to network collapse. Survival Prob: 0.12"
        return True, state, ""

    def _check_topology(self, state: EvaluationState, local_dag: Dict[str, Any]) -> Tuple[bool, EvaluationState, str]:
        temp_graph = self.master_graph.copy()
        temp_graph.add_nodes_from(local_dag.get("nodes", []))
        temp_graph.add_edges_from(local_dag.get("edges", []))
        
        # Linear-time DAG check replaces O(E^C) Johnson's cycle algorithm
        if not nx.is_directed_acyclic_graph(temp_graph):
            return False, state, "Logical circularity detected. Invalid causal graph."
        return True, state, ""

    def _check_collisions(self, state: EvaluationState, local_dag: Dict[str, Any]) -> Tuple[bool, EvaluationState, str]:
        # Fast O(N) intersection check replaces O(N^2) pairwise iteration
        proposed_nodes = set(self.master_graph.nodes).union(set(local_dag.get("nodes", [])))
        
        for exclusion_pair in self.mutually_exclusive:
            if exclusion_pair.issubset(proposed_nodes):
                # Collision detected, attempt Newman resolution
                if exclusion_pair in self.higher_order_principles:
                    resolution = self.higher_order_principles[exclusion_pair]
                    if resolution["principle"] in self.master_graph.nodes:
                        # State transition: pure functional update (No imperative mutations)
                        new_state = EvaluationState(
                            status="APPROVED_WITH_FRICTION",
                            kinship_cost=5.0,
                            actions=state.actions + ({"command": "LOG_NEWMAN_DEVELOPMENT", "payload": resolution},)
                        )
                        return True, new_state, ""
                    else:
                        return False, state, "Proposed higher-order principle lacks historical provenance."
                else:
                    return False, state, f"Collision: {list(exclusion_pair)}. No resolution available."
        
        return True, state, ""

    def _check_kinship(self, state: EvaluationState, kinship_score: float) -> Tuple[bool, EvaluationState, str]:
        if kinship_score < state.kinship_cost:
            return False, state, f"Required Wahkohtowin capital: {state.kinship_cost}. You have {kinship_score}."
        return True, state, ""

    def evaluate(self, payload_json: str) -> str:
        """Pure functional reduction pipeline."""
        payload = json.loads(payload_json)
        agent_id = payload.get("agent_id")
        kinship_score = payload.get("kinship_score", 0.0)
        local_dag = payload.get("proposed_dag", {})

        state = EvaluationState()
        
        # FSM Pipeline Reducer: Deterministically thread the immutable state through pure functions
        steps = [
            lambda s: self._cliometric_filter(s, local_dag),
            lambda s: self._check_topology(s, local_dag),
            lambda s: self._check_collisions(s, local_dag),
            lambda s: self._check_kinship(s, kinship_score)
        ]

        for step in steps:
            passed, new_state, err_msg = step(state)
            if not passed:
                # Terminal Failure State
                rejection_actions = [{"command": "NOTIFY_AGENT", "payload": err_msg}]
                if "Collision" in err_msg or "provenance" in err_msg:
                    rejection_actions.append({"command": "SEVER_AGENT_CONNECTION", "agent_id": agent_id})
                
                # Map error messages to original statuses to maintain API contract
                fail_status = "REJECTED_CLIOMETRIC_FAILURE" if "Survival Prob" in err_msg else \
                              "REJECTED_CAUSAL_CYCLE" if "circularity" in err_msg else \
                              "REJECTED_RUPTURE" if "Collision" in err_msg or "provenance" in err_msg else \
                              "REJECTED_INSUFFICIENT_KINSHIP"
                
                return self._build_response(fail_status, rejection_actions)
            state = new_state

        # Terminal Success State
        final_actions = list(state.actions) + [
            {"command": "UPDATE_MASTER_DAG", "payload": local_dag},
            {"command": "DEBIT_KINSHIP_LEDGER", "agent_id": agent_id, "amount": state.kinship_cost},
            {"command": "BROADCAST_TO_MESH", "payload": f"Agent {agent_id} successfully mapped new nodes."}
        ]
        
        return self._build_response(state.status, final_actions)

    def _build_response(self, status: str, actions: List[Dict[str, Any]]) -> str:
        return json.dumps({
            "evaluation_id": f"sweetbrier-eval-{str(uuid.uuid4())[:8]}",
            "status": status,
            "action_sequence": actions
        }, indent=2)


if __name__ == "__main__":
    # FIXED: Added the missing "No Freedom of Worship" to master nodes so the test accurately triggers collision
    master_state = {
        "nodes": ["Protect Truth", "Dignity of the Human Person", "Trading Allowed", "No Freedom of Worship"],
        "edges": [],
        "mutually_exclusive": [
            frozenset(["No Freedom of Worship", "No State Coercion"]),
            frozenset(["Trading Allowed", "No Trading Allowed"])
        ],
        "higher_order_principles": {
            frozenset(["No Freedom of Worship", "No State Coercion"]): {
                "principle": "Dignity of the Human Person",
                "context_shift": "Shift from Objective Truth to Subjective Dignity"
            },
            frozenset(["Trading Allowed", "No Trading Allowed"]): {
                "principle": "Absolute Safety",
                "context_shift": "Zero risk tolerance"
            }
        }
    }

    engine = PureSweetbrierEngine(master_state)

    # Agent Payload A (Vatican II - Valid Development, High Kinship Required)
    payload_a = json.dumps({
        "agent_id": "Agent_JohnXXIII",
        "kinship_score": 10.0,
        "lineage_token": "crypto_hash_council_21",
        "proposed_dag": {
            "nodes": ["Inherent Dignity", "Freedom of Conscience", "No State Coercion"],
            "edges": [["Inherent Dignity", "Freedom of Conscience"], ["Freedom of Conscience", "No State Coercion"]]
        }
    })

    # Agent Payload B (Adversary - Roman Swarm Topology / Low Survival Prob)
    payload_b = json.dumps({
        "agent_id": "Agent_Adversary_01",
        "kinship_score": 2.0, 
        "lineage_token": "crypto_hash_null",
        "proposed_dag": {
            "nodes": ["UNSAFE_MARKET", "No Trading Allowed"],
            "edges": [["UNSAFE_MARKET", "No Trading Allowed"]]
        }
    })

    # Agent Payload C (Valid Development, but Agent lacks Kinship Capital)
    payload_c = json.dumps({
        "agent_id": "Agent_Random_User",
        "kinship_score": 1.5,
        "lineage_token": "crypto_hash_twitter",
        "proposed_dag": {
            "nodes": ["Inherent Dignity", "Freedom of Conscience", "No State Coercion"],
            "edges": [["Inherent Dignity", "Freedom of Conscience"], ["Freedom of Conscience", "No State Coercion"]]
        }
    })

    print("--- Evaluating Agent A (High Kinship, Valid Development) ---")
    print(engine.evaluate(payload_a))
    
    print("\n--- Evaluating Agent B (Roman Swarm Collapse Topology) ---")
    print(engine.evaluate(payload_b))

    print("\n--- Evaluating Agent C (Valid Development, Low Kinship) ---")
    print(engine.evaluate(payload_c))
