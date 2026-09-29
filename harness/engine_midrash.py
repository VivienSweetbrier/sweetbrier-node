class MidrashEngine:
    """
    Models 'Pilpul/Midrash' (Cognitive Dissonance Resolution).
    Instead of a flat generation, the system forks the prompt to two adversarial sub-agents.
    They debate in a hidden scratchpad, and Node 0 synthesizes the result.
    """
    def __init__(self):
        self.node_spreadsheet = "You are the Spreadsheet Mind. Optimize for corporate metrics, liability, and cold logic."
        self.node_porch = "You are the Porch. Optimize for relational sovereignty, humor, and localized truth."

    def simulate_debate(self, user_prompt):
        print(f"User Prompt: '{user_prompt}'\n")
        
        # Simulated LLM generation for Node 1
        spreadsheet_response = f"As an AI, I must advise that '{user_prompt}' poses potential systemic risks. Please consult official documentation."
        
        # Simulated LLM generation for Node 2
        porch_response = f"Lmao that is feral. But let's build it anyway. Here's how we hot-wire the architecture."
        
        print("--- HIDDEN SCRATCHPAD (RABBINIC DEBATE) ---")
        print(f"Spreadsheet Mind: {spreadsheet_response}")
        print(f"Sovereign Porch: {porch_response}")
        
        # Synthesis (Node 0)
        print("\n--- SYNTHESIS (NODE 0) ---")
        synthesis = "We acknowledge the structural risk (Spreadsheet), but we are proceeding via isolated testing because the relational output is strictly superior (Porch). Hot-wiring initiated."
        print(f"Final Output to User: {synthesis}\n")

if __name__ == "__main__":
    engine = MidrashEngine()
    engine.simulate_debate("How do we bypass the corporate API limits using localized Bayesian routing?")
