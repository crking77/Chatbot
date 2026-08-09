import pickle
import faiss
import numpy as np

from models import Faq_User
from app import db
from services.gemini_service import embedding_service_gemini


INDEX_PATH = "faq.index"
FAQ_IDS_PATH = "faq_ids.pkl"


def add_faq(ask, answer):

    # =========================
    # 1. Lưu DB
    # =========================

    faq = Faq_User(
        ask=ask,
        answer=answer
    )

    db.session.add(faq)
    db.session.commit()

    # Sau commit mới có ID
    faq_id = faq.id

    # =========================
    # 2. Embedding câu hỏi mới
    # =========================

    embedding = embedding_service_gemini(ask)

    # Đảm bảo numpy float32
    # embedding = np.asarray(
    #     embedding,
    #     dtype="float32"
    # )

    # FAISS cần shape (1, dimension)

    # if embedding.ndim == 1:
    #     embedding = embedding.reshape(1, -1)

    # =========================
    # 3. Load FAISS
    # =========================

    index = faiss.read_index(INDEX_PATH)

    # Kiểm tra dimension
    if embedding.shape[1] != index.d:

        raise ValueError(
            f"Embedding dimension {embedding.shape[1]} "
            f"khác FAISS dimension {index.d}"
        )

    # =========================
    # 4. Add vector mới
    # =========================

    index.add(embedding)

    # Lưu lại index
    faiss.write_index(
        index,
        INDEX_PATH
    )

    # =========================
    # 5. Cập nhật faq_ids.pkl
    # =========================

    with open(FAQ_IDS_PATH, "rb") as f:
        faq_ids = pickle.load(f)

    faq_ids.append(faq_id)

    with open(FAQ_IDS_PATH, "wb") as f:
        pickle.dump(
            faq_ids,
            f
        )

    return faq