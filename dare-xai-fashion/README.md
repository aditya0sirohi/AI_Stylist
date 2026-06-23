# AI Fashion Outfit Recommendation System

A small Streamlit app that recommends complete, stylist-curated outfits for a user based on a chat message + a sidebar profile. Built as an internship assignment for Dare XAI.

## What it does

1. You fill in a tiny profile in the sidebar (gender, age, occasion, style).
2. You chat: *"I need an outfit for a wedding cocktail."*
3. Gemini extracts your intent → we filter the catalog → FAISS finds the closest hero item → we look up the full outfit from `outfits.csv` (hero + companions + footwear + accessories) → Gemini explains *why* the outfit works.
4. Streamlit shows the chat reply + product cards with images.

## Architecture overview

```
User (Streamlit chat)
        │
        ▼
Gemini  →  extract intent (JSON: occasion, gender_hint, style keywords)
        │
        ▼
Filter products.csv by gender + occasion
        │
        ▼
sentence-transformers (all-MiniLM-L6-v2)  →  encode query
        │
        ▼
FAISS flat L2 index  →  top-3 hero candidates
        │
        ▼
outfits.csv compatibility map  →  fetch the full curated outfit
        │
        ▼
Gemini  →  write a friendly 3-4 sentence explanation
        │
        ▼
Streamlit  →  chat bubble + product cards
```

A nicer Mermaid version lives in [`architecture.md`](architecture.md).

## Setup

```bash
# 1. clone this repo (or just enter the folder)
cd dare-xai-fashion

# 2. install dependencies
pip install -r requirements.txt

# 3. set the LLM key
#    This project uses the Emergent Universal LLM key (works with Gemini).
#    You can also use a regular GEMINI_API_KEY — llm.py picks up either.
export EMERGENT_LLM_KEY="sk-emergent-..."          # OR
export GEMINI_API_KEY="your-google-gemini-key"

# 4. run
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## How to use

1. Set your profile in the left sidebar.
2. Type something like `I have a beach party next weekend, suggest something light`.
3. Read the assistant reply, click the *Stylist rationale* expander to see the original stylist note from the dataset.

## Tech stack

- **Streamlit** — UI
- **sentence-transformers** (`all-MiniLM-L6-v2`) — text embeddings
- **FAISS** (`IndexFlatL2`) — vector search
- **LangChain** — `ConversationBufferMemory` for chat history
- **Gemini 2.5 Flash** via the `emergentintegrations` Universal LLM key — intent extraction + reply generation
- **pandas** — CSV handling

## Dataset

Cloned from [DarexAI-AI-Startup/ML-TASK](https://github.com/DarexAI-AI-Startup/ML-TASK):
- `products.csv` — 68 fashion items
- `outfits.csv` — 25 stylist-curated outfits (our ground truth for compatibility)
- `images/` — product images

## Known limitations

- **Small dataset** (only 68 products, 25 curated outfits) → coverage is patchy outside the curated outfits.
- **Text-only embeddings** — no visual similarity, so two items that *look* alike but have different metadata won't match.
- **No persistent memory** — chat history lives in `st.session_state` and resets on browser refresh.
- **Gemini model** — using `gemini-2.5-flash` via the Emergent key (assignment originally specified `gemini-1.5-flash`; 2.5-flash is the closest available equivalent and behaves the same way for this task).

## Future improvements

- Swap text embeddings for **CLIP / FashionCLIP** for true multimodal (image + text) retrieval.
- Replace the FAISS flat index with **Qdrant** (or Milvus) once the catalog grows past a few thousand items.
- Add a **user feedback loop** (👍 / 👎 on outfits) and rerank with implicit feedback.
- **Expand the dataset** — 25 outfits is small; richer ground truth = better recommendations.
- **Deploy to Streamlit Cloud** so users don't need a local setup.
