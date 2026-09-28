from google import  genai
import os
import numpy as np
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



def embedding_service_gemini(text):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )
    embedding = np.array(response.embeddings[0].values, dtype=np.float32).reshape(1, -1)
    return embedding

def ask_gemini(question, faqs):
    context = "\n\n".join(
        f"Câu hỏi: {f.ask}\nTrả lời: {f.answer}"
        for f in faqs
    )

    prompt = f"""
Bạn là chatbot tư vấn thủ tục hành chính của Công an xã Hải Châu, tỉnh Nghệ An.
Chỉ được trả lời dựa trên dữ liệu dưới đây.
Không được tự bịa ra câu trả lời khác
Nếu không có thông tin thì nói:
"Chào bạn, bạn cần giải thích rõ hơn để Công an xã hỗ trợ bạn nhé! Hoặc bạn có thể đợi bộ phận chuyên môn trả lời bạn trong thời gian sớm nhất. Xin cảm ơn!"

Dữ liệu:

{context}

Câu hỏi:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text