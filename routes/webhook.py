from flask import Blueprint, request
from config import VERIFY_TOKEN, PAGE_ACCESS_TOKEN
from services.chatbot_service import handle_message

from models import Faq_User
webhook_bp = Blueprint("webhook", __name__)
processed_mid = set()
@webhook_bp.route("/webhook", methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200

        return "Verify Failed", 403
    body = request.get_json()

    if body.get("object") != "page":
        return "OK", 200

    for entry in body.get("entry", []):

        for event in entry.get("messaging", []):

            sender_id = event["sender"]["id"]

            if "message" in event:

                message = event["message"]
                mid = message.get("mid")
                text = message.get("text", "")
            if mid in processed_mid:
                continue
            processed_mid.add(mid)
            handle_message(
                sender_id=sender_id,
                text=text
                )

    return "EVENT_RECEIVED", 200