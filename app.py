from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 👉 从 Render 环境变量读取
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

        # ✅ 2. 获取用户输入
        data = request.get_json(force=True) or {}
        text = data.get("text", "")

        # ✅ 3. NVIDIA API 配置
        url = "https://integrate.api.nvidia.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "nvidia/nemotron-3-ultra-550b-a55b",  # ✅ 你用的模型
            "messages": [
                {
                    "role": "user",
                    "content": f"帮我写一段关于{text}的文案"
                }
            ],
            "max_tokens": 200,
            "stream": False
        }

        # ✅ 4. 发请求
        response = requests.post(url, headers=headers, json=payload)

        # 🔥 关键调试信息（去 Render Logs 看）
        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        # ✅ 5. 尝试解析 JSON
        try:
            result = response.json()
        except:
            return jsonify({
                "error": "NVIDIA返回非JSON",
                "raw": response.text
            }), 500

        # ✅ 6. 解析返回结构
        try:
            content = result["choices"][0]["message"]["content"]
        except:
            return jsonify({
                "error": "返回结构异常",
                "raw": result
            }), 500

        # ✅ 7. 正常返回
        return jsonify({
            "result": content
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ✅ Render 必须这样启动
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
