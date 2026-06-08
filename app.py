from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("NVIDIA_API_KEY")

@app.route("/generate", methods=["POST"])
def generate():
    if not API_KEY:
    raise Exception("Missing NVIDIA_API_KEY")

    try:
        data = request.json or {}
        text = data.get("text", "")

        url = "https://integrate.api.nvidia.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta/llama3-8b-instruct",
            "messages": [
                {"role": "user", "content": f"帮我写一段关于{text}的文案"}
            ],
            "max_tokens": 200
            "stream": False
        }

        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        return jsonify({
            "result": result["choices"][0]["message"]["content"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "NVIDIA backend running!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
