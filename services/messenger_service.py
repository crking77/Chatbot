import requests
# from config import PAGE_ACCESS_TOKEN
GRAPH_URL = "https://graph.facebook.com/v25.0/me/messages"

def send_message(sender_id, text, page_access_token):

    params = {
        "access_token": page_access_token
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