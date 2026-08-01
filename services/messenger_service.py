import requests

GRAPH_URL = "https://graph.facebook.com/v25.0/me/messages"

def send_message(sender_id, text):

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    payload = {
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": text
        }
    }

    requests.post(
        GRAPH_URL,
        params=params,
        json=payload
    )