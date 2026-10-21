import math
import random
import sys
from PIL import Image, ImageDraw, ImageFont

def generate_noise():
    chars = ["0", "1", "+", "!", "|", "-", "=", "*", ".", ":", ";", "/", "\\"]
    return random.choice(chars)

width, height = 80, 26
cell_w, cell_h = 10, 18
img_w = width * cell_w
img_h = height * cell_h

try:
    font = ImageFont.truetype("consola.ttf", 15)
except:
    font = ImageFont.load_default()

frames = []
print("Rendering frames...")
for frame_idx in range(60):
    t = frame_idx * 0.15
    img = Image.new("RGB", (img_w, img_h), (8, 5, 12))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        for x in range(width):
            cx, cy = width / 2.0, height / 2.0
            dx, dy = (x - cx) / 2.0, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            pulse = math.sin(dist - t * 4) + math.sin(t * 2)
            is_cross = (abs(dx) < 2 and abs(dy) < 8) or (abs(dx) < 12 and abs(dy) < 1)
            
            char = " "
            color = (8, 5, 12)
            
            if is_cross and random.random() > 0.1:
                color = (248, 200, 34) if random.random() > 0.05 else (255, 17, 17)
                char = "#" if random.random() > 0.2 else "+"
            elif pulse > 0.8 or (random.random() < 0.02 and dist < 15):
                color = (255, 17, 17) if random.random() > 0.5 else (200, 200, 200)
                char = generate_noise()
            else:
                if random.random() < 0.005:
                    color = (34, 34, 255)
                    char = generate_noise()
                    
            if char != " ":
                draw.text((x * cell_w, y * cell_h), char, fill=color, font=font)
                
    frames.append(img)
    print(f"Frame {frame_idx+1}/60 done.")

gif_path = r"C:\Users\Vivian\.gemini\antigravity\brain\f1e14566-c632-4ff5-9e9f-0b696e1146ea\clankina.gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=60, loop=0)
print("GIF successfully rendered to:", gif_path)
