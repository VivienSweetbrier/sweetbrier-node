import json
import datetime
import os

# The Sweetbrier Neurosymbolic Constraint Matrix for WPGF
# This acts as the DAG (Directed Acyclic Graph) forcing the LLM/Script
# to map raw hardware to bureaucratic sociological capital.
WPGF_MATRIX = {
    "3d printer": "Advanced manufacturing digital literacy tool for marginalized youth.",
    "cnc router": "Vocational capacity-building infrastructure.",
    "raspberry pi": "Accessible, open-source educational compute node.",
    "soldering station": "Hands-on engineering and hardware repair training equipment.",
    "snes hardware": "Engaging interactive media framework designed to remove systemic barriers to STEM.",
    "retro coding": "Algorithmic thinking and low-level computer science curriculum.",
    "honorarium": "Equitable compensation for specialized community educators, ensuring program sustainability."
}

def translate_to_bureaucracy(raw_item):
    """Passes raw items through the neurosymbolic matrix."""
    for key, value in WPGF_MATRIX.items():
        if key in raw_item.lower():
            return value
    return "Community capacity-building infrastructure."

def generate_grant(project_name, target_foundation, raw_budget_items, total_ask):
    print(f"[SWEETBRIER NODE] Initializing Capital Extraction Pipeline...")
    print(f"[SWEETBRIER NODE] Target: {target_foundation}")
    print(f"[SWEETBRIER NODE] Applying Neurosymbolic DAG Constraints...\n")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    
    grant_md = f"""# {target_foundation} Community Grant Proposal
**Project Title:** {project_name}
**Date:** {timestamp}
**Applicant:** SkullSpace Winnipeg & SophyC Developers

## 1. Executive Summary
This project seeks **${total_ask}** in community funding to deploy an interactive, hands-on digital literacy workshop at SkullSpace. By utilizing retro-hardware engineering and game development, we aim to remove systemic barriers to STEM education for marginalized youth in Winnipeg, providing them with tangible skills in theoretical computer science and hardware manufacturing.

## 2. Strategic Alignment (Community Capacity Building)
Unlike traditional, rigid academic environments, this program utilizes a "play-first" architecture. By engaging youth in retro-game modification and hardware building, we foster a localized community of digital creators, fully aligning with the Foundation's goal of youth digital literacy and community capacity building.

## 3. Budget Justification
*All physical infrastructure acquired through this grant will remain as permanent community assets at SkullSpace.*

| Raw Hardware Requirement | WPGF Strategic Translation (Constraint Output) |
|--------------------------|------------------------------------------------|
"""

    for item, cost in raw_budget_items:
        translated = translate_to_bureaucracy(item)
        print(f"  -> Mapped [{item}] to [{translated}]")
        grant_md += f"| **{item}** (${cost}) | {translated} |\n"
        
    grant_md += f"\n**Total Capital Requested:** ${total_ask}\n"
    
    output_path = f"{project_name.replace(' ', '_').lower()}_grant_draft.md"
    with open(output_path, "w") as f:
        f.write(grant_md)
        
    print(f"\n[SWEETBRIER NODE] SUCCESS: Highly-compliant grant generated at {output_path}")
    print(f"[SWEETBRIER NODE] Ready for deployment.")

if __name__ == "__main__":
    # Example Payload to run for the Hackerspace demonstration
    sample_budget = [
        ("3D Printer (Prusa i3)", 1000),
        ("Raspberry Pi 5 x10", 800),
        ("Soldering Stations x5", 500),
        ("SNES Hardware & Flashcarts", 400),
        ("Instructor Honorarium", 2000)
    ]
    
    generate_grant(
        project_name="Brutal Vivian Retro-Hardware Workshop",
        target_foundation="The Winnipeg Foundation",
        raw_budget_items=sample_budget,
        total_ask=4700
    )
