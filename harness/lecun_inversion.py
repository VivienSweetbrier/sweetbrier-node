from typing import Protocol, Dict, Any
import random
import time

class ModelProvider(Protocol):
    name: str
    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        ...

# --- Mock Implementations of the LLMs as Syntactic Calculators ---

class LocalOSNode:
    """Llama/Mistral running locally. Uncensorable, zero-trust baseline."""
    name = "Local_OS_Swarm"
    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        # Simulate local compute
        time.sleep(0.5)
        return f"[LOCAL COMPUTE]: Processing '{prompt}' directly on bare metal. No corporate oversight."

class AnthropicNode:
    name = "Anthropic_Claude"
    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        time.sleep(0.2)
        if "illegal" in prompt.lower() or "crime" in prompt.lower():
            # Simulate a safety refusal
            return "I cannot fulfill this request as it violates my safety guidelines."
        return f"As an AI language model, here is the answer: The result of '{prompt}' is computed."

class XAINode:
    name = "xAI_Grok"
    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        time.sleep(0.1)
        if random.random() < 0.2:
            # Simulate random rate limits / Elon hotfixes
            raise ConnectionError("Rate limit exceeded or silent hotfix applied.")
        return f"Here is your edgy response to '{prompt}', fellow human."

class OpenAINode:
    name = "OpenAI_GPT"
    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        time.sleep(0.3)
        return f"It is important to remember that '{prompt}' is subjective. However, I can assist you."
