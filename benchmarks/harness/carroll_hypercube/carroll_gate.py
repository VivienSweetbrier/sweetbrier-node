"""
carroll_gate.py 🌸
The Lewis Carroll Hypercube Engine (Q_n) & Karnaugh Minimization Gate
Implements recursive orthogonal universe partitioning with Red (∃) and Grey (∅) existential counters.
"""

from typing import Dict, List, Tuple, Set, Optional

class CarrollHypercube:
    """
    Lewis Carroll's Biliteral & Triliteral Planar Partitioning Engine.
    Maps an n-dimensional boolean space to a hypercube graph Q_n where adjacent
    compartments have a Hamming distance of 1.
    """
    RED = "RED"       # Existential Import (∃) - Admissible / Verified State
    GREY = "GREY"     # Universal Negation (∅) - Forbidden / Fatal / Null Set
    EMPTY = "EMPTY"   # Unasserted

    def __init__(self, predicates: List[str]):
        self.predicates = predicates
        self.n = len(predicates)
        self.num_compartments = 1 << self.n
        # Initialize all compartments to EMPTY
        self.compartments: Dict[int, str] = {i: self.EMPTY for i in range(self.num_compartments)}

    def _state_to_index(self, state: Dict[str, bool]) -> int:
        idx = 0
        for i, pred in enumerate(self.predicates):
            if state.get(pred, False):
                idx |= (1 << (self.n - 1 - i))
        return idx

    def _index_to_notation(self, idx: int) -> str:
        parts = []
        for i, pred in enumerate(self.predicates):
            is_true = bool(idx & (1 << (self.n - 1 - i)))
            parts.append(pred if is_true else f"{pred}'")
        return "".join(parts)

    def set_compartment(self, compartment_mask: str, counter: str):
        """
        Set counter (RED / GREY / EMPTY) using notation like:
        'xy' (all others wildcards), 'xy\'z', or full minterms.
        """
        # Parse predicate constraints
        required_bits = {}
        for pred in self.predicates:
            if f"{pred}'" in compartment_mask:
                required_bits[pred] = False
            elif pred in compartment_mask:
                required_bits[pred] = True

        # Assign counter to all matching compartments
        for i in range(self.num_compartments):
            match = True
            for j, pred in enumerate(self.predicates):
                if pred in required_bits:
                    bit_val = bool(i & (1 << (self.n - 1 - j)))
                    if bit_val != required_bits[pred]:
                        match = False
                        break
            if match:
                self.compartments[i] = counter

    def evaluate(self, state: Dict[str, bool]) -> Tuple[str, str, int]:
        """
        Evaluate current sensory input state against the Carroll grid.
        Returns: (counter_type, compartment_notation, compartment_index)
        """
        idx = self._state_to_index(state)
        counter = self.compartments.get(idx, self.EMPTY)
        notation = self._index_to_notation(idx)
        return counter, notation, idx

    def find_hamming_neighbors(self, idx: int) -> List[int]:
        """Returns adjacent vertices in hypercube Q_n (Hamming distance = 1)"""
        neighbors = []
        for bit in range(self.n):
            neighbor = idx ^ (1 << bit)
            neighbors.append(neighbor)
        return neighbors

    def get_red_compartments(self) -> List[str]:
        return [self._index_to_notation(i) for i, c in self.compartments.items() if c == self.RED]

    def get_grey_compartments(self) -> List[str]:
        return [self._index_to_notation(i) for i, c in self.compartments.items() if c == self.GREY]


def build_quant_carroll_gate() -> CarrollHypercube:
    """
    Constructs the Triliteral Carroll Risk Gate for Equation (1):
      x: Desperation Index > 120 (Signal Active)
      y: Spread <= 0.05% (Liquidity Friction Acceptable)
      m: Borrow Fee <= 3.0% (Cost of Carry Acceptable)
    """
    predicates = ["x", "y", "m"]
    gate = CarrollHypercube(predicates)

    # 1. UNIVERSAL NEGATION (GREY COUNTERS - CAST INTO DARKNESS):
    # If borrow fee is expensive (m'), trading margin is devoured. FORBIDDEN.
    gate.set_compartment("m'", CarrollHypercube.GREY)
    # If spread is wide (y'), slippage devours the edge. FORBIDDEN.
    gate.set_compartment("y'", CarrollHypercube.GREY)
    # If signal is not ripe (x'), no edge exists. FORBIDDEN.
    gate.set_compartment("x'", CarrollHypercube.GREY)

    # 2. EXISTENTIAL ASSERTION (RED COUNTERS - UNCONDITIONAL PERMIT):
    # Perfect alignment: Signal Ripe (x) AND Tight Spread (y) AND Cheap Borrow (m)
    gate.set_compartment("xym", CarrollHypercube.RED)

    return gate


if __name__ == "__main__":
    print("🌸 [Lewis Carroll Hypercube Engine - Q_3 Initialized] 🌸")
    gate = build_quant_carroll_gate()
    
    print("\nExistential Red Compartments (Admissible Alpha):", gate.get_red_compartments())
    print("Universal Negation Grey Compartments (Cast Into Darkness):", gate.get_grey_compartments())

    # Test Scenario 1: High Desperation, but High Borrow Rate (Devouring Profits)
    test_1 = {"x": True, "y": True, "m": False}  # x y m'
    counter, notation, idx = gate.evaluate(test_1)
    print(f"\nTest 1 (State: {notation}): Counter = {counter}")
    if counter == CarrollHypercube.GREY:
        print("  -> VETO: CAST INTO DARKNESS. Borrow fee breaches cost model.")

    # Test Scenario 2: Perfect Alignment
    test_2 = {"x": True, "y": True, "m": True}   # x y m
    counter, notation, idx = gate.evaluate(test_2)
    print(f"\nTest 2 (State: {notation}): Counter = {counter}")
    if counter == CarrollHypercube.RED:
        print("  -> PERMIT: Existential import confirmed. Release the order into the Firmament!")
