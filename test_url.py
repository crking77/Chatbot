import requests

url = "http://localhost:5000/webhook"

data = {
    "object": "page",
    "entry": [
        {
            "messaging": [
                {
                    "sender": {"id": "123"},
                    "message": {"text": "Xin chào"}
                }
            ]
        }
    ]
}

r = requests.post(url, json=data)

print(r.status_code)
print(r.text)