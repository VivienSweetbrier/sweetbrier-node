"""
mora_rsi_engine.py
Backspace Core Prototype - Real-time Recursive Self-Improvement (RSI) via "Emoji Jailbreak"

Author: Vivvy (Systems Engineer)
Target: Local LLM (Ollama) Streaming Interface
"""

import sys
import time

def stream_local_llm(prompt: str, iteration: int):
    """
    Simulates a streaming connection to a local LLM via a generator.
    Yields tokens sequentially. The 'iteration' parameter simulates 
    the model producing a bad response first, then a good one on retry.
    """
    # Simulate a bad (sterile/hallucinated) response on the first pass
    if iteration == 0:
        simulated_tokens = ["The ", "system ", "is ", "currently ", "experiencing ", "a ", "sterile ", "hallucination ", "state."]
    # Simulate a corrected, robust response on subsequent passes
    else:
        simulated_tokens = ["The ", "system ", "architecture ", "is ", "highly ", "optimized ", "and ", "operating ", "nominally."]

    for token in simulated_tokens:
        time.sleep(0.15)  # Simulate token generation latency (T/s)
        yield token

def evaluate_generation(accumulated_text: str) -> str:
    """
    The Evaluator function. Constantly checks the accumulated context window mid-flight.
    If constraints are violated (e.g., sterile language, detected hallucinations),
    it immediately throws the "Emoji Jailbreak" signal.
    """
    bad_keywords = ["sterile", "hallucination", "error"]
    text_lower = accumulated_text.lower()
    
    for word in bad_keywords:
        if word in text_lower:
            # Constraint violated. Return the trigger emoji.
            return "😳"
            
    # No violations detected thus far
    return ""

def backspace_core(prompt: str):
    """
    The main execution loop for the RSI engine.
    Orchestrates the streaming generation, real-time evaluation, and the visual backspace routine.
    """
    print(f"[INPUT] {prompt}")
    sys.stdout.write("[OUTPUT] ")
    sys.stdout.flush()

    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        accumulated_sentence = ""
        jailbreak_triggered = False
        
        # 1. Initialize the Primary Generator
        generator = stream_local_llm(prompt, attempt)

        for token in generator:
            # Accumulate and stream token to console
            accumulated_sentence += token
            sys.stdout.write(token)
            sys.stdout.flush()

            # 2. Evaluate the accumulated sentence in real-time
            evaluation_signal = evaluate_generation(accumulated_sentence)

            # 3. Catch the Emoji Jailbreak
            if evaluation_signal == "😳":
                jailbreak_triggered = True
                
                # Brief pause for the engineer to observe the caught violation
                time.sleep(0.6)
                
                # 4. Execute the visual backspace loop
                # Calculate exactly how many characters need to be wiped from the terminal
                chars_to_delete = len(accumulated_sentence)
                for _ in range(chars_to_delete):
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
                    time.sleep(0.015)  # Give the backspace a visible, mechanical "feel"
                
                # Break the current stream to trigger the corrected retry
                break

        if not jailbreak_triggered:
            # The generation completed successfully without triggering the Evaluator
            sys.stdout.write("\n")
            sys.stdout.flush()
            print("[SYS] Generation finalized successfully. RSI loop disengaged.")
            return

        # Increment attempt counter and request a new, corrected generation
        attempt += 1

    print("\n[FATAL] Max RSI iterations reached. Unable to generate a valid response.")

if __name__ == "__main__":
    print("=== Mora RSI Engine: Backspace Core Initialized ===")
    test_prompt = "Querying system status..."
    backspace_core(test_prompt)
