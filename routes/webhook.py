from flask import Blueprint, request
from config import VERIFY_TOKEN
from services.chatbot_service import handle_message
from config import FACEBOOK_PAGE_TOKENS
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
        page_id = entry.get("id")
        page_access_token = FACEBOOK_PAGE_TOKENS.get(page_id)
        if not page_access_token:
            continue  # Skip if the page ID is not found in the tokens dictionary
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
                text=text,
                page_access_token=page_access_token
                )

    return "EVENT_RECEIVED", 200