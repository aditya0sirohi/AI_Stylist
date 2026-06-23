# PRD — AI Fashion Outfit Recommendation System (Dare XAI Internship Task)

## Problem statement
Build a small AI fashion stylist that:
- Takes a free-text request + a sidebar profile (gender, age, occasion, style).
- Recommends a complete outfit (hero + companions + footwear + accessories).
- Explains *why* the outfit works in plain English.
- Uses the `DarexAI-AI-Startup/ML-TASK` dataset (68 products, 25 curated outfits).

## User persona
A junior dev / internship reviewer demoing the project locally. Just clones, sets a key, and runs `streamlit run app.py`.

## Architecture (locked)
- **Streamlit** UI (no React/FastAPI).
- **sentence-transformers (all-MiniLM-L6-v2)** text embeddings.
- **FAISS IndexFlatL2** for vector search (68 vectors — flat is enough).
- **Compatibility graph** built from `outfits.csv` (hero → companions + rationale).
- **Gemini 2.5 Flash** via `emergentintegrations` Universal LLM Key for intent extraction + reply.
- **LangChain `ConversationBufferMemory`** for chat history (single use of LangChain).

## Core flow
1. Bootstrap: load CSVs → embed all products → build FAISS index → build compat map.
2. User chats → Gemini extracts `{occasion, gender_hint, style_keywords, age_group}`.
3. Filter products by gender + occasion → FAISS top-3 → look up hero in compat map.
4. Assemble full outfit → Gemini writes a 3-4 sentence friendly explanation.
5. Streamlit renders chat bubble + product cards + stylist-rationale expander.

## What's implemented (2026-02)
- ✅ `src/utils.py` — CSV loaders, product card formatter
- ✅ `src/embeddings.py` — sentence-transformers + FAISS flat index + filtered search
- ✅ `src/compatibility.py` — hero→outfit map from `outfits.csv`
- ✅ `src/llm.py` — Gemini wrapper (intent extraction + explanation) using Emergent key
- ✅ `src/recommender.py` — filter → search → match → assemble
- ✅ `app.py` — Streamlit UI with sidebar profile + chat + product cards
- ✅ `README.md` + `architecture.md` + `requirements.txt`
- ✅ Dataset copied into `data/` (products.csv, outfits.csv, images/)
- ✅ Verified end-to-end: catalog loads (68 products, 25 outfits), embeddings build (384-dim), Gemini extracts intent JSON, explanation generated, product cards render with images.

## Setup notes
- Run with: `EMERGENT_LLM_KEY=<key> streamlit run app.py` from `/app/dare-xai-fashion/`.
- First run downloads `all-MiniLM-L6-v2` (~80 MB) from HuggingFace.

## Known limitations (documented in README)
- Dataset is small (68 items / 25 outfits).
- Text-only embeddings — no visual similarity.
- Model swap: assignment said `gemini-1.5-flash`, Emergent only exposes `gemini-2.5-flash` (closest stable equivalent).

## Future improvements (P2)
- CLIP / FashionCLIP for multimodal embeddings
- Replace FAISS flat with Qdrant when catalog grows
- Feedback loop (👍 / 👎) and rerank
- Expand dataset
- Deploy to Streamlit Cloud
