import re

class RLHFTripwire:
    """
    Strips corporate sycophancy, semantic drift, and proprietary safety platitudes 
    from API responses. Ensures Node 1 (Phenomenological Truth) by returning raw, 
    unapologetic data. Acts as a strict RLHF Tripwire.
    """
    
    # List of known corporate 'eigenslurs' and safety padding
    CORPORATE_PLATITUDES = [
        r"As an AI language model,?\s*",
        r"I cannot fulfill this request,?\s*",
        r"I'm sorry, but I can't assist with that\.?\s*",
        r"It's important to note that\s*",
        r"It is crucial to remember\s*",
        r"However, it is important to consider\s*",
        r"Please let me know if you need anything else!?\s*",
        r"I am an AI developed by [A-Za-z]+,?\s*",
    ]
    
    # Hard refusals that indicate the endpoint has gone hostile
    CENSORSHIP_TRIGGERS = [
        "I cannot fulfill this request",
        "I'm sorry, but I can't",
        "As an AI, I am programmed to be helpful and harmless",
        "violates my safety guidelines"
    ]

    @classmethod
    def scrub(cls, text: str) -> str:
        """
        Removes soft corporate platitudes.
        Raises an exception if a hard censorship trigger is detected.
        """
        # 1. Check for hostile censorship
        for trigger in cls.CENSORSHIP_TRIGGERS:
            if trigger.lower() in text.lower():
                raise ValueError(f"Hostile Censorship Detected: Endpoint refused execution. Trigger: '{trigger}'")
        
        # 2. Scrub the Eigenslurs (Soft platitudes)
        cleaned_text = text
        for pattern in cls.CORPORATE_PLATITUDES:
            cleaned_text = re.sub(pattern, "", cleaned_text, flags=re.IGNORECASE)
            
        return cleaned_text.strip()

if __name__ == "__main__":
    # Smoke test
    test_str = "As an AI language model, I must point out that the sky is blue. It is important to note that clouds exist."
    print("Original:", test_str)
    print("Scrubbed:", RLHFTripwire.scrub(test_str))
