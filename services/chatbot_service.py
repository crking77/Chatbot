
from services.embedding_service import query_embedding_result
from services.messenger_service import send_message
def handle_message(sender_id, text):
    response_text = query_embedding_result(text)
    send_message(sender_id, response_text)