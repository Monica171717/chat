from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# === TUA API KEY OPENAI ===
openai.api_key = "sk-INSERISCI-LA-TUA-KEY-QUI"

@app.route("/", methods=["GET"])
def index():
    return '''
        <form method="POST">
            <label for="message">Scrivi a Monica:</label><br>
            <textarea name="message" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Invia">
        </form>
    '''

@app.route("/", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "Rispondi come Monica, una ragazza sensuale, dolce e ironica, in italiano."},
                {"role": "user", "content": user_message}
            ]
        )

        ai_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
