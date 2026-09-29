
from services.messenger_service import send_message
from services.embedding_service import query_embedding_result
import threading
from collections import defaultdict
from flask import current_app
message_buffer = defaultdict(list)
message_timers = {}

def process_messages(sender_id, app):

    messages = message_buffer.pop(
        sender_id,
        []
    )
    message_timers.pop(sender_id,None)
    if not messages:
        return

    combined_text = " ".join(item["text"] for item in messages)
    page_access_token = messages[0]["page_access_token"]
    print("[PROCESS]",sender_id,combined_text)
    with app.app_context():
        response_text = query_embedding_result(combined_text)
        send_message(sender_id, response_text, page_access_token)


def add_message(sender_id, text, page_access_token):
    app = current_app._get_current_object()
    # Thêm tin nhắn vào danh sách
    print("[ADD_MESSAGE] START")
    print("[ADD_MESSAGE]", sender_id, text)
    message_buffer[sender_id].append({"text": text, "page_access_token": page_access_token})
    # Nếu đã có timer thì hủy timer cũ
    old_timer = message_timers.get(sender_id)
    if old_timer:
        old_timer.cancel()

    # Tạo timer mới 60 giây
    timer = threading.Timer(
        60,
        process_messages,
        args=(sender_id,app)
    )

    message_timers[sender_id] = timer

    timer.start()

    print(
        f"[BUFFER] {sender_id}: {text}"
    )