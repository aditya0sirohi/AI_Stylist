# AI Stylist — Multi-Project Repository

A collection of AI-powered fashion and styling projects, featuring a production-ready **AI Fashion Outfit Recommendation System** built with Streamlit, vector search, and LLMs.

---

## 📁 What's Inside

### **1. dare-xai-fashion/** — 🎯 Main Project
An AI-powered fashion stylist that recommends complete outfits based on user preferences and occasion.

**Tech Stack:**
- **Streamlit** — Interactive UI
- **Sentence-Transformers** (`all-MiniLM-L6-v2`) — Text embeddings
- **FAISS** — Vector similarity search (68 items)
- **Gemini 2.5 Flash** (via Emergent Universal LLM Key) — Intent extraction + outfit explanations
- **LangChain** — Conversation history (ConversationBufferMemory)
- **pandas** — Data handling

**Dataset:**
- 68 fashion items (products.csv)
- 25 stylist-curated outfits (outfits.csv)
- Product images

**How it works:**
1. User fills sidebar profile (gender, age, occasion, style preference)
2. Types a request: *"I need an outfit for a beach party"*
3. Gemini extracts intent → FAISS finds similar hero item → looks up full outfit from compatibility map
4. Streamlit renders chat reply + product cards + styling rationale

**Quick Start:**
```bash
cd dare-xai-fashion
export EMERGENT_LLM_KEY="sk-emergent-..." # or GEMINI_API_KEY
pip install -r requirements.txt
streamlit run app.py
```

Open browser → `http://localhost:8501`

**Learn More:** See [`dare-xai-fashion/README.md`](dare-xai-fashion/README.md) and [`dare-xai-fashion/architecture.md`](dare-xai-fashion/architecture.md)

---

### **2. backend/** — FastAPI + MongoDB Template
A minimal FastAPI server with async MongoDB support.

**Includes:**
- FastAPI with CORS middleware
- Motor (async MongoDB driver)
- Pydantic models with validation
- Status check API endpoints (`POST /api/status`, `GET /api/status`)
- Environment variable configuration

**Quick Start:**
```bash
cd backend
pip install -r requirements.txt
export MONGO_URL="mongodb://..." DB_NAME="ai_stylist"
uvicorn server:app --reload
```

**API Docs:** `http://localhost:8000/docs`

---

### **3. frontend/** — React + Tailwind Scaffolding
A Create React App template with Tailwind CSS and shadcn/ui configuration (currently empty scaffolding).

**Setup (if needed):**
```bash
cd frontend
npm install
npm start
```

**Status:** This is a starter scaffold. Customize or remove if not needed.

---

## 📋 Project Requirements

See [`memory/PRD.md`](memory/PRD.md) for the original project requirements and design decisions.

---

## 🛠️ Development

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- Gemini API key (or Emergent Universal LLM key)
- MongoDB connection string (for backend)

### Environment Variables

Create a `.env` file in the project root or in `backend/`:

```bash
# LLM Keys
EMERGENT_LLM_KEY="sk-emergent-..."  # OR
GEMINI_API_KEY="your-gemini-key"

# MongoDB (for backend)
MONGO_URL="mongodb://localhost:27017"
DB_NAME="ai_stylist"

# Backend
CORS_ORIGINS="http://localhost:3000,http://localhost:8501"
```

---

## 🎯 What's Working

✅ **dare-xai-fashion** — Fully functional  
- Loads catalog, builds embeddings, runs recommendation pipeline
- Chat UI with product cards and styling explanations  
- Works end-to-end with Gemini

✅ **backend** — Template ready  
- FastAPI server with MongoDB integration  
- Async I/O for scalability  

⚠️ **frontend** — Scaffolding only  
- Empty React app (boilerplate)  
- Configure as needed for your use case

---

## 🚀 Next Steps

1. **Use dare-xai-fashion as-is** — It's production-ready for local deployment
2. **Expand backend** — Add auth, chat API, user preferences storage
3. **Build frontend** — Connect React to backend + Streamlit via API, or build a standalone UI
4. **Deploy** — Streamlit Cloud (free tier available), Vercel, or Docker

---

## 📖 Documentation

- [`dare-xai-fashion/README.md`](dare-xai-fashion/README.md) — Full system docs
- [`dare-xai-fashion/architecture.md`](dare-xai-fashion/architecture.md) — Data flow diagrams
- [`memory/PRD.md`](memory/PRD.md) — Original requirements & design decisions

---

## 🤝 Contributing

This is a personal project. Feel free to refactor, extend, or remix the modules as needed.

---

## 📄 License

Not specified. Add a LICENSE file if publishing.

---

## ✨ Built with
- [Streamlit](https://streamlit.io/) — UI framework
- [FAISS](https://github.com/facebookresearch/faiss) — Vector search
- [Sentence-Transformers](https://www.sbert.net/) — Embeddings
- [FastAPI](https://fastapi.tiangolo.com/) — API framework
- [React](https://react.dev/) — Web UI
