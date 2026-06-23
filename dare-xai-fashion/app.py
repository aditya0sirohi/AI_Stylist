"""
app.py
Streamlit UI for the AI Fashion Outfit Recommendation System.
Keeps state in st.session_state, talks to src/* for the heavy lifting.
"""

import os
import sys

import streamlit as st
from langchain.memory import ConversationBufferMemory

# make `src` importable when running `streamlit run app.py`
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils import load_products, load_outfits
from src.embeddings import embed_products, build_faiss_index
from src.compatibility import build_compatibility_map
from src.llm import extract_intent, generate_explanation
from src.recommender import recommend


# ----------------------------- config -----------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PRODUCTS_CSV = os.path.join(DATA_DIR, "products.csv")
OUTFITS_CSV = os.path.join(DATA_DIR, "outfits.csv")


st.set_page_config(
    page_title="AI Fashion Stylist",
    page_icon="👗",
    layout="wide",
)


# ----------------------------- caching ----------------------------------
# Streamlit re-runs the whole script on every interaction, so we cache
# the expensive loads behind @st.cache_resource (kept across sessions).
@st.cache_resource(show_spinner="Loading products and building embeddings...")
def bootstrap():
    products_df = load_products(PRODUCTS_CSV)
    outfits_df = load_outfits(OUTFITS_CSV)
    embeddings = embed_products(products_df)
    index = build_faiss_index(embeddings)
    compat_map = build_compatibility_map(outfits_df)
    return products_df, outfits_df, index, compat_map


products_df, outfits_df, faiss_index, compat_map = bootstrap()


# ----------------------------- session init -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    # LangChain memory — we only really use this to show "we used LangChain".
    st.session_state.memory = ConversationBufferMemory(return_messages=True)


# ----------------------------- sidebar profile --------------------------
with st.sidebar:
    st.markdown("### Your Style Profile")
    name = st.text_input("Name", value="Friend", key="profile_name")
    gender = st.selectbox("Gender", ["women", "men"], key="profile_gender")
    age = st.slider("Age", 16, 60, 25, key="profile_age")
    occasion = st.selectbox(
        "Occasion",
        ["casual", "office", "party", "wedding", "beach", "formal"],
        key="profile_occasion",
    )
    style_preference = st.selectbox(
        "Style preference",
        ["minimal", "classic", "trendy", "bold", "ethnic"],
        key="profile_style",
    )

    st.markdown("---")
    st.caption(f"Catalog: **{len(products_df)}** products, "
               f"**{len(outfits_df)}** curated outfits")

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.memory.clear()
        st.rerun()


profile = {
    "name": name,
    "gender": gender,
    "age": age,
    "occasion": occasion,
    "style_preference": style_preference,
}


# ----------------------------- header -----------------------------------
st.title("AI Fashion Stylist")
st.caption("Tell me where you're going — I'll put together a complete outfit.")


# ----------------------------- chat history -----------------------------
def render_cards(cards):
    if not cards:
        return
    cols = st.columns(min(len(cards), 4))
    for i, card in enumerate(cards):
        with cols[i % len(cols)]:
            if card["image_path"]:
                st.image(card["image_path"], use_container_width=True)
            else:
                st.markdown("*(no image)*")
            st.markdown(f"**{card['name']}**")
            st.caption(f"{card['brand']} · ₹{card['price_inr']}")
            st.caption(f"_{card['category_label']} · {card['occasion']}_")


# replay existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("cards"):
            render_cards(msg["cards"])
        if msg.get("rationale"):
            with st.expander("Stylist rationale (from curated outfit)"):
                st.write(msg["rationale"])


# ----------------------------- chat input -------------------------------
user_input = st.chat_input("e.g. I need an outfit for a business meeting tomorrow")

if user_input:
    # 1) show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.memory.chat_memory.add_user_message(user_input)
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2) extract intent + recommend
    with st.chat_message("assistant"):
        with st.spinner("Putting together your outfit..."):
            intent = extract_intent(user_input)
            result = recommend(
                products_df=products_df,
                faiss_index=faiss_index,
                compat_map=compat_map,
                user_message=user_input,
                intent=intent,
                profile=profile,
                data_dir=DATA_DIR,
            )

            explanation = generate_explanation(
                user_message=user_input,
                profile=profile,
                outfit_details=result["outfit_text"],
                stylist_rationale=result.get("rationale", ""),
            )

        st.markdown(explanation)
        render_cards(result["cards"])
        if result.get("rationale"):
            with st.expander("Stylist rationale (from curated outfit)"):
                st.write(result["rationale"])

    st.session_state.memory.chat_memory.add_ai_message(explanation)
    st.session_state.messages.append({
        "role": "assistant",
        "content": explanation,
        "cards": result["cards"],
        "rationale": result.get("rationale", ""),
    })
