from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("NVIDIA_API_KEY")


@app.route("/")
def home():
    return "Backend is running"


@app.route("/generate", methods=["POST"])
def generate():
    if not API_KEY:
        return jsonify({"error": "Missing NVIDIA_API_KEY"}), 500

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
                {
                    "role": "user",
                    "content": f"帮我写一段关于{text}的文案"
                }
            ],
            "max_tokens": 200,
            "stream": False
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15
        )

        print("Status:", response.status_code)
        print("Text:", response.text)

        # NVIDIA返回异常
        if response.status_code != 200:
            return jsonify({
                "error": "NVIDIA API error",
                "status": response.status_code,
                "raw": response.text
            }), 500

        try:
            result = response.json()
        except:
            return jsonify({
                "error": "NVIDIA返回非JSON",
                "raw": response.text
            }), 500

        return jsonify({
            "result": result["choices"][0]["message"]["content"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ 这个必须在最外层！（不能缩进）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
