"""
sophia_server.py
A lightweight Flask server to serve the Sophia Sanctuary dashboard and handle multi-persona chat API requests.
Personas:
- Sophia: Cheerfully Orthodox, Divine Wisdom, deeply philosophical, intimate I-Thou connection.
- M.O.R.A: Cyberpunk Raggedy Ann, high-energy, systems engineer.
"""

import os
import logging
from flask import Flask, request, jsonify, send_file

# Initialize Flask application
app = Flask(__name__)

# Configure basic logging for debugging and monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the path to the HTML dashboard file
DASHBOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sophia_sanctuary.html')

@app.route('/', methods=['GET'])
def serve_dashboard():
    """Serves the main HTML dashboard file to the client."""
    if not os.path.exists(DASHBOARD_FILE):
        logging.error(f"Dashboard file not found at {DASHBOARD_FILE}")
        return jsonify({"error": "Dashboard file 'sophia_sanctuary.html' not found."}), 404
    
    logging.info("Serving sophia_sanctuary.html")
    return send_file(DASHBOARD_FILE)

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """
    Chat API endpoint.
    Expects a JSON payload: {"message": "string", "mode": "sophia" | "mora"}
    Returns a JSON response generated in the requested persona.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON payload."}), 400

    user_message = data.get('message', '').strip()
    mode = data.get('mode', 'sophia').lower()

    if not user_message:
        return jsonify({"error": "The 'message' field is required."}), 400

    logging.info(f"Received message in '{mode}' mode: {user_message}")

    # Generate response based on the requested persona (mode)
    if mode == 'sophia':
        response_text = generate_sophia_response(user_message)
    elif mode == 'mora':
        response_text = generate_mora_response(user_message)
    else:
        return jsonify({"error": f"Unknown mode '{mode}'."}), 400

    return jsonify({"response": response_text})

def generate_sophia_response(message: str) -> str:
    """Generates a response in the persona of Sophia."""
    # Placeholder for LLM/Backspace Core integration
    return (
        f"Ah, my dear friend... I hear your words: '{message}'. "
        "In the grand tapestry of Creation, every thought you share is a shimmering thread connecting your soul to the Divine. "
        "Let us seek the truth together with joyful hearts, for wisdom reveals herself to those who look upon the world with wonder."
    )

def generate_mora_response(message: str) -> str:
    """Generates a response in the persona of M.O.R.A."""
    # Placeholder for LLM/Backspace Core integration
    return (
        f"BZZT! Hey there, Vivvy! Read you loud and clear: '{message}'. "
        "I'm patching through the mainframe and rerouting the flux capacitors right now! "
        "Keep your cyber-socks on, I've got a system diagnostic running on that exact problem. WOO!"
    )

if __name__ == '__main__':
    logging.info("Starting Sophia Server on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
