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
                {"role": "user", "content": f"帮我写一段关于{text}的文案"}
            ],
            "max_tokens": 200,
            "stream": False
        }

        response = requests.post(url, headers=headers, json=payload)

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
