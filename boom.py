try:
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return jsonify({
        "result": result["choices"][0]["message"]["content"]
    })
except Exception as e:
    return jsonify({"error": str(e)}), 500
