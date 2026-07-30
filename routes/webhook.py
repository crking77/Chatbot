from flask import Blueprint, request
from config import VERIFY_TOKEN
from services.chatbot import process_message

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/webhook", methods=["GET"])
def verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification Failed", 403


@webhook_bp.route("/webhook", methods=["POST"])
def receive():

    body = request.get_json()

    print("=" * 60)
    print(body)
    print("=" * 60)

    if body.get("object") != "page":
        return "OK", 200

    for entry in body.get("entry", []):

        for event in entry.get("messaging", []):

            sender_id = event["sender"]["id"]

            if "message" not in event:
                continue

            message = event["message"]

            if "text" in message:

                text = message["text"]

                print(f"Sender : {sender_id}")
                print(f"Message: {text}")

                process_message(sender_id, text)

    return "EVENT_RECEIVED", 200