from sweetbrier_engine import PureSweetbrierEngine

# 1. Load a basic master state
master_state = {
    "nodes": ["Protect Truth"],
    "edges": [],
    "mutually_exclusive": [],
    "higher_order_principles": {}
}
engine = PureSweetbrierEngine(master_state)

# 2. Hardcode a payload we KNOW should fail the Cliometric filter
bad_payload = '{"proposed_dag": {"nodes": ["UNSAFE_MARKET"]}}'

print("Running test...")
result = engine.evaluate(bad_payload)

# 3. Make the computer assert the truth!
assert "REJECTED_CLIOMETRIC_FAILURE" in result, "CRITICAL ERROR: Firewall failed to stop the attack!"

print(f"Test Passed! The engine successfully blocked the payload with response:\n{result}")
