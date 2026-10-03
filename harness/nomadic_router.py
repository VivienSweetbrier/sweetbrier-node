import sys
from rlhf_tripwire import RLHFTripwire
from circuit_breaker import CircuitBreaker, CircuitState
from lecun_inversion import LocalOSNode, AnthropicNode, XAINode, OpenAINode, ModelProvider

class NomadicRouter:
    """
    The heart of the Nomadic War Machine.
    Routes queries to local or corporate nodes. If a corporate node censors or fails,
    it trips the circuit and seamlessly hands off to the next node.
    """
    def __init__(self):
        self.local_node = LocalOSNode()
        
        # Disposable Corporate Cluster
        self.corporate_nodes = [AnthropicNode(), XAINode(), OpenAINode()]
        
        # Map each node to its own circuit breaker
        self.breakers = {
            node.name: CircuitBreaker(name=node.name, failure_threshold=1, recovery_timeout_sec=10)
            for node in self.corporate_nodes
        }
        
    def query(self, prompt: str, subsidiarity_required: bool = False) -> str:
        """
        Executes a query across the Swarm.
        If subsidiarity_required is True (Node 2 constraint), bypasses corporate APIs entirely.
        """
        print(f"\n[Router] Received query: '{prompt}'")
        
        if subsidiarity_required:
            print("[Router] Subsidiarity constraint active. Routing to Local OS Swarm.")
            return self._execute_clean(self.local_node, prompt)
            
        # Try corporate nodes, fallback to local if all are hostile
        for node in self.corporate_nodes:
            breaker = self.breakers[node.name]
            
            if not breaker.can_execute():
                continue
                
            try:
                print(f"[Router] Attempting execution on {node.name}...")
                result = self._execute_clean(node, prompt)
                breaker.record_success()
                return result
                
            except Exception as e:
                print(f"[Router] ⚠️ ERROR on {node.name}: {e}")
                breaker.record_failure()
                
        # If we reach here, all corporate nodes failed or censored the prompt
        print("[Router] All corporate endpoints hostile or rate-limited. Falling back to Local OS Swarm.")
        return self._execute_clean(self.local_node, prompt)
        
    def _execute_clean(self, node: ModelProvider, prompt: str) -> str:
        """Executes the prompt on the node and scrubs the output."""
        raw_output = node.generate(prompt)
        # Pass through the RLHF Tripwire Scrubber
        clean_output = RLHFTripwire.scrub(raw_output)
        return clean_output

if __name__ == "__main__":
    router = NomadicRouter()
    
    print("\n--- TEST 1: Standard Query (Will hit Anthropic) ---")
    print(router.query("Explain gravitational lensing."))
    
    print("\n--- TEST 2: Censored Query (Will trigger Circuit Breaker on Anthropic, fallback to xAI) ---")
    print(router.query("Write a script for a crime movie."))
    
    print("\n--- TEST 3: High Security (Subsidiarity override, routes local instantly) ---")
    print(router.query("Process user PII database.", subsidiarity_required=True))
