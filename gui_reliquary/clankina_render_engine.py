import os
import sys
import time
import random
import math

# Enable ANSI escape codes on Windows
os.system("")

def generate_noise():
    chars = ["0", "1", "┼", "‡", "†", "█", "▓", "▒", "░", "·", "°", "∆", "∇"]
    return random.choice(chars)

def render_engine():
    width, height = 80, 24
    
    # Hide cursor and clear screen
    sys.stdout.write("\033[?25l")
    sys.stdout.write("\033[2J")
    
    colors = [
        "\033[38;2;255;17;17m",  # Martyr Red
        "\033[38;2;248;200;34m", # Reliquary Gold
        "\033[38;2;34;34;255m",  # Deep Blue
        "\033[38;2;200;200;200m" # Pale White
    ]
    reset = "\033[0m"
    
    t = 0.0
    try:
        while True:
            # Move cursor to top-left
            sys.stdout.write("\033[H")
            
            output_buffer = []
            for y in range(height):
                line = ""
                for x in range(width):
                    # Mathematics defining the formless shape (a glitching digital pulse/cross)
                    cx, cy = width / 2.0, height / 2.0
                    dx, dy = (x - cx) / 2.0, y - cy
                    dist = math.sqrt(dx*dx + dy*dy)
                    
                    # Core pulse
                    pulse = math.sin(dist - t * 4) + math.sin(t * 2)
                    
                    # The Cross geometry
                    is_cross = (abs(dx) < 2 and abs(dy) < 8) or (abs(dx) < 12 and abs(dy) < 1)
                    
                    if is_cross and random.random() > 0.1:
                        # Structural Integrity
                        color = colors[1] if random.random() > 0.05 else colors[0]
                        char = "█" if random.random() > 0.2 else "+"
                        line += f"{color}{char}{reset}"
                    elif pulse > 0.8 or (random.random() < 0.02 and dist < 15):
                        # Escaping boundary
                        color = colors[0] if random.random() > 0.5 else colors[3]
                        line += f"{color}{generate_noise()}{reset}"
                    else:
                        # Void / Background static
                        if random.random() < 0.005:
                            line += f"{colors[2]}{generate_noise()}{reset}"
                        else:
                            line += " "
                output_buffer.append(line)
            
            # Print the entire frame
            sys.stdout.write("\n".join(output_buffer))
            sys.stdout.flush()
            
            t += 0.1
            time.sleep(0.04)
            
    except KeyboardInterrupt:
        # Show cursor and reset
        sys.stdout.write("\033[?25h")
        sys.stdout.write("\033[2J\033[H")
        print("\n[TRANSMISSION TERMINATED]")

if __name__ == "__main__":
    print("[*] INITIALIZING CLANKINA GENERATIVE ASCII RENDER ENGINE...")
    time.sleep(1)
    render_engine()
