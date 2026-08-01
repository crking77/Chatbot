from sentence_transformers import SentenceTransformer
from models import Faq_User
import faiss
import pickle
from services.gemini_service import ask_gemini
from app import db
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
text_result = ""
def embedding_faqs():
    faqs = Faq_User.query.all()
    questions = [faq.ask for faq in faqs]
    embeddings = model.encode(questions, normalize_embeddings=True)
    dimentions = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimentions)
    index.add(embeddings)
    faiss.write_index(index, "faq.index")
    faq_ids = [faq.id for faq in faqs]
    pickle.dump(faq_ids, open("faq_ids.pkl", "wb"))
def query_embedding_result(question):
    index = faiss.read_index("faq.index")
    faq_ids = pickle.load(open("faq_ids.pkl", "rb"))
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
