# Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- A Gemini API key or Emergent Universal LLM key

## Installation

### Step 1: Clone & Navigate
```bash
git clone https://github.com/aditya0sirohi/AI_Stylist.git
cd AI_Stylist/dare-xai-fashion
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set API Key
```bash
export EMERGENT_LLM_KEY="sk-emergent-..."  # OR
export GEMINI_API_KEY="your-gemini-key"
```

On Windows (PowerShell):
```powershell
$env:EMERGENT_LLM_KEY="sk-emergent-..."
```

### Step 5: Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## First Run

1. **Set your profile** in the left sidebar:
   - Name
   - Gender (men/women)
   - Age range
   - Occasion (casual, office, party, wedding, beach, formal)
   - Style preference (minimal, classic, trendy, bold, ethnic)

2. **Try a prompt:**
   - *"I need an outfit for a beach party next weekend"*
   - *"Suggest something for a casual Friday at the office"*
   - *"I have a wedding to attend, what should I wear?"*

3. **Explore the results:**
   - See the AI-generated explanation
   - Click product cards to see details
   - Expand "Stylist rationale" to see why the outfit was chosen

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:** Ensure you're in the virtual environment and ran `pip install -r requirements.txt`

### Issue: `API key error` or `Authentication failed`
**Solution:** Check your API key is set correctly:
```bash
echo $EMERGENT_LLM_KEY  # Check if set
```

### Issue: `FAISS index error`
**Solution:** Delete `.cache/` folder and restart. The embeddings will rebuild on next run.

---

## Architecture Overview

See [`architecture.md`](dare-xai-fashion/architecture.md) for detailed data flow diagrams.

**High-level flow:**
1. User profile + chat input → Gemini extracts intent
2. Filter products by gender + occasion
3. FAISS finds similar hero item (via embeddings)
4. Look up full outfit from compatibility map
5. Streamlit renders outfit cards + explanation

---

## Dataset

- **68 fashion products** (products.csv)
- **25 curated outfits** (outfits.csv) mapping hero items to complete looks
- **Product images** in data/images/

Source: [DarexAI-AI-Startup/ML-TASK](https://github.com/DarexAI-AI-Startup/ML-TASK)

---

## Next Steps

- Expand the dataset for better coverage
- Swap text embeddings for CLIP/FashionCLIP (multimodal)
- Add user feedback loop (👍 / 👎)
- Deploy to Streamlit Cloud
- Build a web API wrapper for integration

---

## Need Help?

Check [`dare-xai-fashion/README.md`](dare-xai-fashion/README.md) for full documentation.
