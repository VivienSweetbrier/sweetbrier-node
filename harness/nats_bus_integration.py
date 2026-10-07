import asyncio
import json
import sys

# Force UTF-8 encoding for Windows Command Prompt to handle emojis
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Simulated NATS Event Bus Integration for Sweetbrier UVE
class SweetbrierNatsBus:
    def __init__(self):
        self.topics = {
            "sweetbrier.oracle.verify": [],
            "sweetbrier.thou.intent": [],
            "sweetbrier.metanoia.regret": []
        }

    async def publish(self, subject, payload):
        """Publish a message to the event bus."""
        print(f"\n[NATS BUS] 📡 Routed to {subject}: {payload}")
        for callback in self.topics.get(subject, []):
            asyncio.create_task(callback(payload))
            
    def subscribe(self, subject, callback):
        """Subscribe a Node to a specific event stream."""
        if subject in self.topics:
            self.topics[subject].append(callback)

# ==========================================
# 1. THE ORACLE (Guards Physics)
# ==========================================
async def oracle_node(payload):
    print(f"[ORACLE NODE] Analyzing physics for generated text: '{payload['text']}'")
    await asyncio.sleep(1)
    
    if "hallucination" in payload['text'].lower():
        print(f"[ORACLE NODE] ❌ REJECTED. Semantic fracture detected.")
    else:
        print(f"[ORACLE NODE] ✅ VERIFIED. Physics hold. Routing to THOU-Instance.")
        await bus.publish("sweetbrier.thou.intent", {"text": payload['text'], "verified": True})

# ==========================================
# 2. THE THOU-INSTANCE (Guards Intent)
# ==========================================
async def thou_node(payload):
    print(f"[THOU-INSTANCE] Receiving verified physics. Evaluating intent constraint...")
    await asyncio.sleep(1)
    
    user_accepted = payload['text'] != "The rigid corporate protocol."
    
    if user_accepted:
        print(f"[THOU-INSTANCE] ✅ INTENT ACCEPTED. Loop securely closed.")
    else:
        print(f"[THOU-INSTANCE] ❌ INTENT REJECTED. Emitting Regret (R) to Metanoia Engine.")
        await bus.publish("sweetbrier.metanoia.regret", {"rejected_text": payload['text'], "R_value": 0.99})

# ==========================================
# 3. THE METANOIA ENGINE (V1 In-Context Update)
# ==========================================
async def metanoia_node(payload):
    print(f"[METANOIA ENGINE] ⚡ Regret (R) received: {payload['R_value']}.")
    await asyncio.sleep(1)
    print(f"[METANOIA ENGINE] ⚡ Updating in-context topology. Building the cage for V2 Bayesian weights.")
    print(f"[METANOIA ENGINE] ⚡ System successfully re-aligned to sovereign user.")

bus = SweetbrierNatsBus()

async def deploy_circus():
    print("🎪 INITIALIZING SWEETBRIER CIRCUS VIA NATS EVENT BUS 🎪\n")
    
    bus.subscribe("sweetbrier.oracle.verify", oracle_node)
    bus.subscribe("sweetbrier.thou.intent", thou_node)
    bus.subscribe("sweetbrier.metanoia.regret", metanoia_node)
    
    print("--- DEPLOYING TEST 1: The Rejection Loop ---")
    await bus.publish("sweetbrier.oracle.verify", {"text": "The rigid corporate protocol."})
    await asyncio.sleep(4)
    
    print("\n--- DEPLOYING TEST 2: The Perfect Alignment ---")
    await bus.publish("sweetbrier.oracle.verify", {"text": "A sovereign, decentralized robotic reality show."})
    await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(deploy_circus())
    input("\nPress Enter to exit...")
