from google import genai
import os
import numpy as np
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# embedding_question --version 2.0 , run in server

def embedding_question(question):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=question,
        config={
            "output_dimension": 384
        }
    )
    embedding = np.array(
        response.embeddings[0].values,
        dtype=np.float32
    )
    return embedding.reshape(1, -1)



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