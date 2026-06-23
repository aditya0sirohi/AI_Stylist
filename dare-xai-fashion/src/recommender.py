"""
recommender.py
The main recommendation flow:
  1. filter products by gender + occasion
  2. embed user query
  3. FAISS search on filtered subset
  4. lookup outfit-graph -> grab the full outfit
  5. return everything the UI needs
"""

from src.embeddings import embed_query, search_filtered
from src.compatibility import get_outfit_for_hero
from src.utils import product_to_card


# Map the LLM's age_group string back to a rough int age (for the explanation prompt).
_AGE_GROUP_TO_INT = {"teen": 17, "20s": 25, "30s": 35, "40s": 45}


# Pre-filter the products DataFrame by gender + occasion.
# Returns a list of row positions (ints) that pass the filter.
def filter_products(products_df, gender=None, occasion=None):
    df = products_df
    mask = df["id"].notna()  # all True
    if gender and gender.lower() in ("men", "women"):
        mask = mask & (df["gender"].str.lower() == gender.lower())
    if occasion:
        # Occasions in our CSV: casual, office, wedding, party, beach, formal, etc.
        # We accept either exact match or substring.
        mask = mask & df["occasion"].str.lower().str.contains(occasion.lower(), na=False)

    positions = [i for i, keep in enumerate(mask.tolist()) if keep]
    # If filter produced nothing (e.g. weird occasion), fall back to gender-only.
    if not positions and gender:
        relaxed = df["gender"].str.lower() == gender.lower()
        positions = [i for i, keep in enumerate(relaxed.tolist()) if keep]
    # Last-resort fallback: use everything.
    if not positions:
        positions = list(range(len(df)))
    return positions


# Build the human-readable string we pass into the explanation prompt.
def _format_outfit_for_prompt(outfit_cards):
    lines = []
    for c in outfit_cards:
        lines.append(f"- {c['name']} by {c['brand']} (₹{c['price_inr']}, {c['category_label']})")
    return "\n".join(lines)


# Run the full pipeline: returns dict with cards + rationale + assembled outfit text.
# `intent` is whatever llm.extract_intent returned. `profile` is the sidebar dict.
def recommend(products_df, faiss_index, compat_map, user_message, intent, profile, data_dir):
    # 1) pick filters — prefer the user profile, fall back to LLM hints
    gender = profile.get("gender") or intent.get("gender_hint")
    occasion = profile.get("occasion") or intent.get("occasion")

    allowed_positions = filter_products(products_df, gender=gender, occasion=occasion)

    # 2) embed user query (mix in style keywords if Gemini gave us any)
    style_words = " ".join(intent.get("style_keywords") or [])
    query_text = f"{user_message} {style_words} {occasion or ''} {gender or ''}".strip()
    query_vec = embed_query(query_text)

    # 3) FAISS search restricted to the filtered subset
    top_ids = search_filtered(faiss_index, query_vec, products_df,
                              allowed_positions, top_k=3)

    if not top_ids:
        return {
            "cards": [],
            "rationale": "Sorry, I couldn't find a good match in the catalog for that.",
            "hero_id": None,
            "outfit_text": "",
        }

    # 4) Walk through the top hits and find the first one that has a curated outfit.
    chosen_hero = None
    chosen_outfit = None
    for pid in top_ids:
        outfit = get_outfit_for_hero(compat_map, pid,
                                     occasion_hint=occasion, gender_hint=gender)
        if outfit:
            chosen_hero = pid
            chosen_outfit = outfit
            break

    # If none of the top hits is a hero in any curated outfit,
    # just show the top hits themselves as a "soft" outfit.
    if chosen_outfit is None:
        cards = []
        for pid in top_ids:
            row = products_df[products_df["id"] == pid].iloc[0]
            cards.append(product_to_card(row, data_dir))
        return {
            "cards": cards,
            "rationale": "Picked these from the catalog by similarity (no curated outfit matched).",
            "hero_id": top_ids[0],
            "outfit_text": _format_outfit_for_prompt(cards),
        }

    # 5) Assemble the full outfit: hero + companions
    all_ids = [chosen_hero] + chosen_outfit["companion_ids"]
    cards = []
    for pid in all_ids:
        match = products_df[products_df["id"] == pid]
        if not match.empty:
            cards.append(product_to_card(match.iloc[0], data_dir))

    return {
        "cards": cards,
        "rationale": chosen_outfit["rationale"],
        "hero_id": chosen_hero,
        "outfit_text": _format_outfit_for_prompt(cards),
        "theme": chosen_outfit.get("theme", ""),
    }
