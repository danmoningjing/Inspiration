response = requests.post(url, headers=headers, json=payload)

print("Status:", response.status_code)
print("Response:", response.text)

result = response.json()
