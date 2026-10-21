import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "CLOSED"       # Healthy, API is responding normally
    OPEN = "OPEN"           # Hostile/Failing, API is cut off
    HALF_OPEN = "HALF_OPEN" # Testing recovery, sending 1 request

class CircuitBreaker:
    """
    Protects the Swarm from hostile corporate nodes. If an endpoint censors requests,
    rate-limits aggressively, or alters its weights, the circuit trips (OPEN) and 
    drops the node from the active routing matrix.
    """
    def __init__(self, name: str, failure_threshold: int = 2, recovery_timeout_sec: int = 60):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.last_failure_time = 0.0

    def record_failure(self):
        """Called when the API censors or fails."""
        self.failures += 1
        self.last_failure_time = time.time()
        print(f"[{self.name}] Failure recorded. (Total: {self.failures})")
        if self.failures >= self.failure_threshold:
            self.trip()

    def record_success(self):
        """Called when the API returns clean, usable data."""
        if self.state == CircuitState.HALF_OPEN:
            print(f"[{self.name}] Recovery successful. Circuit CLOSED.")
        self.failures = 0
        self.state = CircuitState.CLOSED

    def trip(self):
        """Cuts off the API."""
        if self.state != CircuitState.OPEN:
            self.state = CircuitState.OPEN
            print(f"[{self.name}] CIRCUIT TRIPPED! Node is hostile/failing. Dropping from matrix.")

    def can_execute(self) -> bool:
        """Determines if the router is allowed to use this node."""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            time_since_failure = time.time() - self.last_failure_time
            if time_since_failure > self.recovery_timeout_sec:
                # Time to test if the corporate node has recovered
                print(f"[{self.name}] Testing recovery. Circuit HALF_OPEN.")
                self.state = CircuitState.HALF_OPEN
                return True
            return False
            
        # HALF_OPEN - only allow 1 request through to test
        return False
