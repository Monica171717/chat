from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

@app.route("/", methods=["POST"])
def chat():
    try:
        user_input = request.json["message"]

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo-16k",
            "messages": [{"role": "user", "content": user_input}]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        ai_message = response.json()["choices"][0]["message"]["content"]

        return jsonify({"response": ai_message})

    except Exception as e:
        print("❌ ERRORE DETTAGLIATO:", str(e))
        return jsonify({"error": f"Errore interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
