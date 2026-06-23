import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from src.utils import build_product_text


_model = None


def get_model():
    """Load sentence transformer model (lazy load)."""
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_products(products_df):
    """Create embeddings for all products."""
    model = get_model()
    texts = [build_product_text(row) for _, row in products_df.iterrows()]
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.astype("float32")


def build_faiss_index(embeddings):
    """Build FAISS index from embeddings."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


def embed_query(query_text):
    """Embed a single query string."""
    model = get_model()
    vec = model.encode([query_text], show_progress_bar=False, convert_to_numpy=True)
    return vec.astype("float32")


def search_filtered(index, query_vec, products_df, allowed_positions, top_k=3):
    """Search index and filter by allowed positions."""
    if len(allowed_positions) == 0:
        return []

    search_k = min(len(products_df), max(top_k * 5, 15))
    distances, indices = index.search(query_vec, search_k)

    allowed_set = set(allowed_positions)
    results = []
    for pos in indices[0]:
        if pos in allowed_set:
            results.append(products_df.iloc[pos]["id"])
            if len(results) >= top_k:
                break
    return results
