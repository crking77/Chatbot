from google import genai
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_gemini(question, faqs):
    context = "\n\n".join(
        f"Câu hỏi: {f.ask}\nTrả lời: {f.answer}"
        for f in faqs
    )

    prompt = f"""
Bạn là chatbot tư vấn thủ tục hành chính của Công an xã Hải Châu, tỉnh Nghệ An.
Chỉ được trả lời dựa trên dữ liệu dưới đây.
Nếu không có thông tin thì nói:
"Chào bạn, bạn cần giải thích rõ hơn để Công an xã hỗ trợ bạn nhé!."

Dữ liệu:

{context}

Câu hỏi:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text