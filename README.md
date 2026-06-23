# AI Stylist

AI Stylist is a fashion recommendation system that generates complete outfit suggestions from natural language requests. The project was built as part of an internship assignment and combines semantic search, curated outfit mappings, and large language models to produce explainable outfit recommendations.

The repository also contains optional backend and frontend scaffolding for future expansion.

---

## Repository Structure

```
AI-Stylist/
│
├── dare-xai-fashion/      # Main application
├── backend/               # FastAPI + MongoDB template
├── frontend/              # React + Tailwind scaffold
└── memory/PRD.md          # Project requirements and design notes
```

---

## Main Project: AI Fashion Outfit Recommendation System

The primary application is located in `dare-xai-fashion/`.

### Overview

The system recommends complete outfits based on:

* User profile information
* Occasion
* Style preferences
* Natural language requests

Rather than recommending isolated products, the application retrieves stylist-curated outfits consisting of clothing, footwear, and accessories that are known to work together.

### Features

* Conversational outfit recommendations
* Semantic search using vector embeddings
* Curated outfit compatibility mapping
* Occasion-aware recommendations
* Personalized styling explanations
* Interactive Streamlit interface
* Product image display

---

## System Architecture

```
User Request
      │
      ▼
Gemini Intent Extraction
      │
      ▼
Catalog Filtering
      │
      ▼
Sentence Embeddings
      │
      ▼
FAISS Similarity Search
      │
      ▼
Outfit Compatibility Lookup
      │
      ▼
Gemini Explanation Generation
      │
      ▼
Streamlit Response
```

### Recommendation Pipeline

1. User provides profile information:

   * Gender
   * Age
   * Occasion
   * Preferred style

2. User submits a natural language request.

3. Gemini extracts structured intent information from the query.

4. Relevant products are filtered from the catalog.

5. Query embeddings are generated using Sentence Transformers.

6. FAISS retrieves the closest matching hero item.

7. The outfit compatibility map is used to assemble the complete outfit.

8. Gemini generates a natural language explanation describing why the recommendation works.

---

## Technology Stack

| Component           | Technology                                 |
| ------------------- | ------------------------------------------ |
| UI                  | Streamlit                                  |
| Embeddings          | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector Search       | FAISS                                      |
| LLM                 | Gemini 2.5 Flash                           |
| Conversation Memory | LangChain                                  |
| Data Processing     | Pandas                                     |

---

## Dataset

The project uses a small curated fashion dataset consisting of:

| File           | Description                         |
| -------------- | ----------------------------------- |
| `products.csv` | Product catalog                     |
| `outfits.csv`  | Stylist-curated outfit combinations |
| `images/`      | Product images                      |

Current dataset size:

* 68 fashion products
* 25 curated outfits

---

## Running the Application

### Prerequisites

* Python 3.9+
* Gemini API key or Emergent Universal LLM key

### Installation

```bash
cd dare-xai-fashion

pip install -r requirements.txt
```

### Environment Variables

```bash
export EMERGENT_LLM_KEY="your-key"
```

or

```bash
export GEMINI_API_KEY="your-key"
```

### Start the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## Example Query

```
I need an outfit for a beach party next weekend.
```

The system will:

* Identify the occasion
* Retrieve the most relevant outfit
* Display recommended items
* Explain the styling rationale

---

## Backend Template

The `backend/` directory contains a FastAPI starter project with MongoDB integration.

### Included

* FastAPI
* Motor (async MongoDB driver)
* Pydantic validation
* CORS support
* Sample API endpoints
* Environment-based configuration

### Run

```bash
cd backend

pip install -r requirements.txt

export MONGO_URL="mongodb://localhost:27017"
export DB_NAME="ai_stylist"

uvicorn server:app --reload
```

API documentation:

```
http://localhost:8000/docs
```

---

## Frontend Scaffold

The `frontend/` directory contains a React and Tailwind setup intended for future development.

Current status:

* React application scaffold
* Tailwind configuration
* shadcn/ui setup

No application-specific features have been implemented yet.

---

## Current Limitations

### Dataset Size

The recommendation quality is constrained by the limited number of products and curated outfits.

### Text-Only Retrieval

Similarity search relies entirely on product metadata and descriptions. Visual similarity between products is not considered.

### Session-Based Memory

Conversation history is stored only for the active Streamlit session and is lost after refresh.

### Scalability

FAISS `IndexFlatL2` works well for small catalogs but is not ideal for large-scale production inventories.

---

## Future Improvements

* Multimodal retrieval using CLIP or FashionCLIP
* Qdrant or Milvus for large-scale vector search
* User feedback collection and reranking
* Expanded fashion catalog
* User authentication and profile persistence
* Cloud deployment
* Recommendation analytics
* Inventory-aware recommendations

---

## Design Decisions

This project intentionally combines:

* LLMs for understanding user intent
* Embeddings for semantic retrieval
* Curated stylist knowledge for compatibility

The goal is to avoid purely generative recommendations and instead ground responses in outfit combinations that have been explicitly curated.

---

## License

No license has been specified for this repository.
