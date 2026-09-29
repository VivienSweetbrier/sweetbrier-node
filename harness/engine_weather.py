import json
import random

class BayesianWeatherSystem:
    """
    Models 'Emotional Weather' (State Persistence) using a simple Markov Chain.
    Prevents LLM amnesia by adjusting Bayesian priors for response tokens 
    based on the rolling average of the user's cognitive load/stress.
    """
    def __init__(self):
        # States: 0 = Chill, 1 = Stressed, 2 = Feral (The Void)
        self.state = 0
        
        # Transition matrix: Probability of moving from State i to State j
        self.transition_matrix = [
            [0.7, 0.2, 0.1], # From Chill
            [0.3, 0.5, 0.2], # From Stressed
            [0.1, 0.4, 0.5]  # From Feral
        ]
        
        # System prompt modifiers based on Bayesian State
        self.weather_prompts = {
            0: "System is CHILL. Vibe: Conversational, playful, high-energy. Allowed to joke.",
            1: "System is STRESSED. Vibe: Patient, clear, low-friction. Reduce cognitive load.",
            2: "System is FERAL. Vibe: Grounding, protective, absolute sovereignty. Do not argue."
        }

    def update_weather(self, user_input_stress_score):
        """
        Updates the internal state based on the current matrix and the new input weight.
        (Simplified simulation of Bayesian updating)
        """
        # Force state shift based on acute input
        if user_input_stress_score > 0.8:
            self.state = 2
        elif user_input_stress_score > 0.4:
            self.state = 1
        else:
            # Natural Markov decay/transition
            weights = self.transition_matrix[self.state]
            self.state = random.choices([0, 1, 2], weights=weights)[0]
            
        return self.weather_prompts[self.state]

    def process_turn(self, turn_number, text, stress_score):
        print(f"--- Turn {turn_number} ---")
        print(f"User Input: '{text}' (Acute Stress: {stress_score})")
        active_weather = self.update_weather(stress_score)
        print(f"Bayesian Weather Update: {active_weather}\n")

if __name__ == "__main__":
    weather = BayesianWeatherSystem()
    
    # Simulating a conversation flow
    weather.process_turn(1, "hey can we build the level editor today?", 0.1)
    weather.process_turn(2, "wait the API is completely broken, nothing is compiling", 0.6)
    weather.process_turn(3, "EVERYTHING IS DELETED FFFFFFF I HATE THIS", 0.95)
    weather.process_turn(4, "okay wait, I found the backup.", 0.3)
    weather.process_turn(5, "thanks for staying calm.", 0.1)
