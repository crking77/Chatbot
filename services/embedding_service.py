from sentence_transformers import SentenceTransformer
import faiss
import pickle
from models import Faq_User
from services.gemini_service import ask_gemini
from app import db



index = faiss.read_index("faq.index")
with open("faq_ids.pkl", "rb") as f:
    faq_ids = pickle.load(f)
text_result = "Chào bạn, bạn cần giải thích rõ hơn để Công an xã hỗ trợ bạn nhé!."
def embedding_faqs():
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    faqs = Faq_User.query.all()
    questions = [faq.ask for faq in faqs]
    embeddings = model.encode(questions, normalize_embeddings=True)
    dimentions = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimentions)
    index.add(embeddings)
    faiss.write_index(index, "faq.index")
    faq_ids = [faq.id for faq in faqs]
    pickle.dump(faq_ids, open("faq_ids.pkl", "wb"))


# query_embedding_result --version 1.0 , run in local
def query_embedding_result(question):
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    question_embedding = model.encode([question], normalize_embeddings=True)
    D, I = index.search(question_embedding, k=5)
    score = float(D[0][0])
    top_faqs = []
    for idx in I[0]:
        if idx != -1:
            faq = db.session.get(Faq_User, faq_ids[idx])
            if faq:
                top_faqs.append(faq)
    if score < 0.8:
        return  ask_gemini(question, top_faqs)
    if top_faqs:
        text_result = top_faqs[0].answer
    return text_result

# query_embedding_result --version 2.0 , run in server
# def query_embedding_result(question):
#     question_embedding = embedding_question(question)
#     print("FAISS dimension:", index.d)
#     print("Question dimension:", question_embedding.shape)
#     D, I = index.search(question_embedding, k=5)
#     score = float(D[0][0])
#     top_faqs = []
#     for idx in I[0]:
#         if idx != -1:
#             faq = db.session.get(Faq_User, faq_ids[idx])
#             if faq:
#                 top_faqs.append(faq)
#     if score < 0.8:
#         return  ask_gemini(question, top_faqs)
#     if top_faqs:
#         text_result = top_faqs[0].answer
#     return text_result