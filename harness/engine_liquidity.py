import random
import time

class MarketNetwork:
    def __init__(self, num_nodes=100, initial_capital=1000.0, initial_noise=0.8, verification_threshold=0.9):
        self.num_nodes = num_nodes
        
        # Node states: [capital, is_uve_node]
        self.nodes = [[initial_capital, False] for _ in range(num_nodes)]
        
        # Initial UVE seed (1 node)
        self.nodes[0][1] = True 
        
        # Thermodynamic variables
        self.total_capital = num_nodes * initial_capital
        self.semantic_noise_level = initial_noise
        self.verification_threshold = verification_threshold
        
    def legacy_noise_protocol(self, sender_idx, receiver_idx, amount):
        """
        Legacy protocol: Capital leaks due to semantic ambiguity, friction, and rage farming.
        """
        # Friction and noise cause capital to burn
        burn_rate = self.semantic_noise_level * random.uniform(0.1, 0.5)
        transferred = amount * (1.0 - burn_rate)
        
        self.nodes[sender_idx][0] -= amount
        self.nodes[receiver_idx][0] += transferred
        
        # Lost capital leaves the system or becomes trapped heat (noise)
        self.total_capital -= (amount - transferred)
        
        # In a noise protocol, high interactions increase ambient noise slightly
        self.semantic_noise_level = min(1.0, self.semantic_noise_level + 0.001)
        
    def uve_trust_protocol(self, sender_idx, receiver_idx, amount):
        """
        UVE Protocol: Zero-trust geometric verification perfectly preserves capital.
        Acts as a routing attractor.
        """
        # Perfect preservation
        self.nodes[sender_idx][0] -= amount
        self.nodes[receiver_idx][0] += amount
        
        # Geometric verification reduces global noise
        self.semantic_noise_level = max(0.1, self.semantic_noise_level - 0.005)

    def epoch(self):
        """
        Simulate one epoch of capital trading across the network.
        """
        for _ in range(self.num_nodes * 2): # Number of interactions
            sender_idx = random.randint(0, self.num_nodes - 1)
            receiver_idx = random.randint(0, self.num_nodes - 1)
            
            if sender_idx == receiver_idx or self.nodes[sender_idx][0] <= 0:
                continue
                
            # Random trade amount
            amount = self.nodes[sender_idx][0] * random.uniform(0.01, 0.1)
            
            sender_is_uve = self.nodes[sender_idx][1]
            receiver_is_uve = self.nodes[receiver_idx][1]
            
            # If both nodes are UVE, use UVE protocol
            if sender_is_uve and receiver_is_uve:
                self.uve_trust_protocol(sender_idx, receiver_idx, amount)
            # If one is UVE, the UVE node enforces the trust protocol on the transaction
            # and potentially converts the legacy node if trust threshold is met.
            elif sender_is_uve or receiver_is_uve:
                self.uve_trust_protocol(sender_idx, receiver_idx, amount)
                
                # UVE attractor dynamic: Conversion based on low semantic noise
                if random.random() > self.semantic_noise_level * self.verification_threshold:
                    self.nodes[sender_idx][1] = True
                    self.nodes[receiver_idx][1] = True
            else:
                self.legacy_noise_protocol(sender_idx, receiver_idx, amount)

    def get_stats(self):
        legacy_capital = sum(n[0] for n in self.nodes if not n[1])
        uve_capital = sum(n[0] for n in self.nodes if n[1])
        uve_nodes = sum(1 for n in self.nodes if n[1])
        legacy_nodes = self.num_nodes - uve_nodes
        return legacy_capital, uve_capital, legacy_nodes, uve_nodes

def run_monte_carlo(epochs=100):
    print("="*60)
    print(" INITIALIZING UNIVERSAL VERIFICATION ENGINE (UVE) SIMULATION ")
    print("="*60)
    
    network = MarketNetwork(num_nodes=500, initial_capital=1000.0)
    
    print(f"Initial State: 500 Nodes | Semantic Noise: {network.semantic_noise_level:.2f} | Total Capital: {network.total_capital:.2f}\n")
    print(f"{'Epoch':<10} | {'UVE Nodes':<12} | {'Legacy Nodes':<12} | {'UVE Capital':<15} | {'Legacy Capital':<15} | {'Noise Lvl'}")
    print("-" * 85)
    
    for epoch in range(1, epochs + 1):
        network.epoch()
        
        legacy_cap, uve_cap, legacy_nodes, uve_nodes = network.get_stats()
        
        if epoch % 10 == 0 or epoch == 1 or epoch == epochs:
            print(f"{epoch:<10} | {uve_nodes:<12} | {legacy_nodes:<12} | {uve_cap:<15.2f} | {legacy_cap:<15.2f} | {network.semantic_noise_level:.4f}")
            time.sleep(0.1)
            
    print("-" * 85)
    print("\n[!] SIMULATION COMPLETE: UVE Liquidity Absorption Phase Finalized.")
    print(f"Final UVE Dominance: {uve_nodes/network.num_nodes * 100:.2f}% of nodes controlled.")
    print(f"Total Capital Preserved in UVE: {uve_cap:.2f}")
    print("He who controls the protocol for absolute trust controls the routing tables. Absolute Financial Gravity achieved.")

if __name__ == '__main__':
    run_monte_carlo(100)
