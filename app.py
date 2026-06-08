from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("NVIDIA_API_KEY")


@app.route("/")
def home():
    return "Backend is running!"


@app.route("/generate", methods=["POST"])
def generate():
    try:
        # ✅ 1. 检查 API KEY
        if not API_KEY:
            return jsonify({"error": "Missing NVIDIA_API_KEY"}), 500

        # ✅ 2. 解析请求 JSON
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")

        # ✅ 3. NVIDIA API
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

        response = requests.post(url, headers=headers, json=payload)

        # ✅ 4. 关键：防炸 JSON
        try:
            result = response.json()
        except:
            return jsonify({
                "error": "NVIDIA返回非JSON",
                "raw": response.text
            }), 500

        # ✅ 5. 解析结果（再防一次）
        try:
            content = result["choices"][0]["message"]["content"]
        except:
            return jsonify({
                "error": "返回格式异常",
                "raw": result
            }), 500

        return jsonify({"result": content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
