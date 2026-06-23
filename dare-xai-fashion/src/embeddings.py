"""
embeddings.py
Builds sentence-transformer embeddings for all products and a FAISS flat index.
Tiny dataset (68 items) so a flat L2 index is more than enough.
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from src.utils import build_product_text


# Module-level cache so we don't reload the model every call.
_model = None


# Lazily load the sentence-transformer model (downloads ~80MB on first run).
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# Embed all products in the DataFrame and return a numpy array of shape (N, dim).
def embed_products(products_df):
    model = get_model()
    texts = [build_product_text(row) for _, row in products_df.iterrows()]
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.astype("float32")


# Build a FAISS flat L2 index from a (N, dim) embedding matrix.
def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


# Embed a single user query string and return a (1, dim) numpy array.
def embed_query(query_text):
    model = get_model()
    vec = model.encode([query_text], show_progress_bar=False, convert_to_numpy=True)
    return vec.astype("float32")


# Search the FAISS index restricted to a list of row positions (filtered subset).
# Returns the product IDs from products_df ordered by similarity (closest first).
def search_filtered(index, query_vec, products_df, allowed_positions, top_k=3):
    if len(allowed_positions) == 0:
        return []

    # Search more than we need, then keep only those in the allowed set.
    # 68 items is tiny so we can over-search safely.
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
