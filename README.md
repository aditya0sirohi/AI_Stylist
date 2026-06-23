# AI Stylist

AI Stylist is an AI-powered fashion recommendation system that suggests complete outfits based on user preferences, occasion, and natural language requests.

The project combines semantic search, curated outfit compatibility data, and large language models to generate explainable outfit recommendations through a conversational interface.

Developed as part of the Dare XAI Machine Learning & AI Engineer Internship Assignment.

---

## Repository Structure

```text
dare-xai-fashion/
│
├── data/
│   ├── products.csv
│   ├── outfits.csv
│   └── images/
│
├── src/
│   ├── compatibility.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── recommender.py
│   └── utils.py
│
├── app.py
├── architecture.md
├── requirements.txt
│
├── README.md
└── SETUP.md
```

---

## Overview

The system recommends stylist-curated outfits rather than individual products.

A user provides:

* Gender
* Age
* Occasion
* Style preference
* Natural language request

Example:

```text
I need an outfit for a beach party next weekend.
```

The application identifies the user's intent, retrieves the most relevant outfit from the catalog, and generates a styling explanation.

---

## Features

* Conversational outfit recommendations
* Semantic search using vector embeddings
* Occasion-aware outfit selection
* Curated outfit compatibility mapping
* LLM-powered intent extraction
* AI-generated styling explanations
* Interactive Streamlit interface
* Product image support

---

## System Architecture

### High-Level Flow

```text
User Request
      │
      ▼
Intent Extraction (LLM)
      │
      ▼
Semantic Retrieval
      │
      ▼
Outfit Assembly
      │
      ▼
Explanation Generation
      │
      ▼
UI Rendering
```

### Module-Level Architecture

```text
User
 │
 ▼
app.py
 │
 ▼
llm.py
(Intent Extraction)
 │
 ▼
recommender.py
 │
 ├── embeddings.py
 │      ├─ Sentence Transformers
 │      └─ FAISS Search
 │
 └── compatibility.py
        └─ Outfit Matching Logic
 │
 ▼
llm.py
(Styling Explanation)
 │
 ▼
app.py
(Display Results)
```

---

## Recommendation Pipeline

### 1. User Input

The user provides profile information through the Streamlit sidebar and enters a request in the chat interface.

### 2. Intent Extraction

`llm.py` uses Gemini to extract structured information such as:

* Occasion
* Style preference
* Gender hints
* Relevant keywords

### 3. Product Retrieval

`embeddings.py` converts the query into an embedding using:

```text
all-MiniLM-L6-v2
```

The embedding is searched against a FAISS index to find the most relevant products.

### 4. Outfit Construction

`compatibility.py` retrieves the complete outfit associated with the selected hero item using curated outfit mappings from `outfits.csv`.

### 5. Explanation Generation

Gemini generates a concise explanation describing why the outfit fits the user's request.

### 6. Presentation

`app.py` displays:

* Recommended products
* Product images
* Outfit details
* Styling rationale

---

## Technology Stack

| Component           | Technology            |
| ------------------- | --------------------- |
| Frontend            | Streamlit             |
| Embeddings          | Sentence Transformers |
| Embedding Model     | all-MiniLM-L6-v2      |
| Vector Search       | FAISS                 |
| LLM                 | Gemini 2.5 Flash      |
| Conversation Memory | LangChain             |
| Data Processing     | Pandas                |

---

## Dataset

The project uses a curated fashion dataset consisting of:

| File         | Description                         |
| ------------ | ----------------------------------- |
| products.csv | Product catalog                     |
| outfits.csv  | Stylist-curated outfit combinations |
| images/      | Product images                      |

Current dataset size:

* 68 products
* 25 curated outfits

---

## Installation

### Prerequisites

* Python 3.9+
* Gemini API Key or Emergent Universal LLM Key

### Clone Repository

```bash
git clone <repository-url>
cd dare-xai-fashion
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

```bash
export EMERGENT_LLM_KEY="your-key"
```

or

```bash
export GEMINI_API_KEY="your-key"
```

### Run Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Example Query

```text
I need something formal for a wedding reception.
```

### Example Workflow

```text
User Query
     │
     ▼
Extract Intent
     │
     ▼
Generate Embedding
     │
     ▼
Search FAISS Index
     │
     ▼
Select Hero Product
     │
     ▼
Retrieve Matching Outfit
     │
     ▼
Generate Styling Explanation
     │
     ▼
Display Recommendation
```

---

## Current Limitations

### Limited Dataset

The recommendation quality depends heavily on the available catalog and curated outfit combinations.

### Text-Based Retrieval

Recommendations are based on metadata and textual descriptions rather than visual similarity.

### Session Memory Only

Conversation history exists only for the active Streamlit session and is not persisted.

### Small-Scale Retrieval

FAISS IndexFlatL2 works well for small catalogs but would require replacement for significantly larger inventories.

---

## Future Improvements

* FashionCLIP or CLIP-based multimodal retrieval
* Qdrant or Milvus vector database integration
* User feedback and preference learning
* Expanded fashion catalog
* Persistent user profiles
* Recommendation analytics
* Cloud deployment
* Personalized outfit history

---

## Design Choices

This project intentionally combines:

* LLMs for intent understanding
* Vector search for semantic retrieval
* Curated outfit mappings for compatibility

Instead of generating outfits entirely through an LLM, recommendations are grounded in stylist-approved outfit combinations, helping maintain consistency and compatibility.

---

## License

No license has been specified for this project.
