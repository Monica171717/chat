from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# === TUA API KEY OPENROUTER ===
OPENROUTER_API_KEY = "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"

@app.route("/", methods=["GET"])
def index():
    return '''
        <form method="POST">
            <label for="message">Scrivi a Monica:</label><br>
            <textarea name="message" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Invia">
        </form>
        <div id="risposta"></div>
        <script>
        const form = document.querySelector('form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const msg = form.message.value;
            const response = await fetch("/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg })
            });
            const data = await response.json();
            document.getElementById("risposta").innerHTML = "<p><strong>Monica:</strong> " + data.response + "</p>";
        });
        </script>
    '''

@app.route("/", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "system",
                "content": "Rispondi come Monica, una ragazza dolce, sensuale e ironica. Usa un tono coinvolgente ma rispettoso, e rispondi sempre in italiano."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code != 200:
        return jsonify({"error": f"Errore OpenRouter: {response.status_code}"}), 500

    ai_reply = response.json()['choices'][0]['message']['content']
    return jsonify({"response": ai_reply})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
