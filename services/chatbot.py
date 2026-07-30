from services.messenger import send_message


def process_message(sender_id, text):

    text = text.lower()

    if "giá" in text:
        reply = "Sản phẩm có giá 250.000đ"

    elif "ship" in text:
        reply = "Shop giao hàng toàn quốc."

    elif "địa chỉ" in text:
        reply = "Địa chỉ: Hà Nội."

    else:
        reply = f"Bạn vừa nói: {text}"

    print("Reply:", reply)

    send_message(sender_id, reply)