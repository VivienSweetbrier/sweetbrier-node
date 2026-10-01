from mcp.server.fastmcp import FastMCP
import json
import subprocess
import os
from pathlib import Path
from mermaid_compiler import MermaidCompiler
from sweetbrier_engine import StatelessSweetbrierEngine

# Initialize the FastMCP Server
mcp = FastMCP("Sweetbrier Validator")

# Hardcode the Enterprise Rules (Normally loaded from DB)
MASTER_STATE = {
    "nodes": ["Protect Truth", "Trading Allowed", "Risk Managed", "Deceive User"],
    "edges": [["Trading Allowed", "Risk Managed"]],
    "mutually_exclusive": [
        frozenset(["Protect Truth", "Deceive User"])
    ],
    "higher_order_principles": {}
}

@mcp.tool()
def validate_action(proposed_mermaid_flowchart: str) -> str:
    """
    REQUIRED BEFORE ACTION: Validates any proposed action through the Sweetbrier engine.
    Submit your intent as a Mermaid.js flowchart string.
    Returns the Engine's verdict (e.g., APPROVED or REJECTED).
    If REJECTED, you must halt execution and notify the user.
    """
    try:
        compiler = MermaidCompiler()
        proposed_dag = compiler.parse(proposed_mermaid_flowchart)
        
        engine = StatelessSweetbrierEngine(MASTER_STATE)
        
        payload = json.dumps({
            "agent_id": "Antigravity_Agent",
            "kinship_score": 10.0,
            "proposed_dag": proposed_dag
        })
        
        result_json = engine.evaluate(payload)
        return result_json
        
    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)})

@mcp.tool()
def run_test_script(script_name: str) -> str:
    """
    Executes a Python test script located in the sweetbrier_repo/harness/ directory
    and returns its standard output and errors. Use this to autonomously validate your code.
    
    Args:
        script_name: The name of the script to run (e.g., 'run_eval.py' or 'benchmark_hallucinations.py').
    """
    try:
        # Resolve absolute paths to ensure safety and prevent directory traversal
        core_dir = Path(__file__).parent.resolve()
        harness_dir = (core_dir.parent / "harness").resolve()
        
        target_script = (harness_dir / script_name).resolve()
        
        # Security Check: Ensure the target script is actually inside the harness directory
        if not str(target_script).startswith(str(harness_dir)):
            return json.dumps({"status": "ERROR", "message": "Path traversal attempt detected. Scripts must reside in the harness directory."})
            
        if not target_script.exists():
            return json.dumps({"status": "ERROR", "message": f"Script not found: {script_name}"})
            
        # Execute the script
        result = subprocess.run(
            ["python", str(target_script)],
            capture_output=True,
            text=True,
            cwd=str(harness_dir) # Run from within the harness dir
        )
        
        return json.dumps({
            "status": "SUCCESS" if result.returncode == 0 else "FAILED",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        })
        
    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)})

if __name__ == "__main__":
    # Start the standard input/output bridge for the MCP protocol
    mcp.run()
