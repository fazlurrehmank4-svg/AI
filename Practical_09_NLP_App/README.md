# Practical 09: Multilingual Domain-Specific Agricultural & Weather NLP Chatbot (CropGuard AI)

## Overview
CropGuard AI Assistant is a high-performance, local agricultural and meteorological conversational agent providing zero-latency advice across **English**, **Hindi (हिंदी)**, and **Urdu (اردو)** without relying on external or paid LLM APIs.

---

## Urdu AI Architecture & Training Pipeline
Adapted from the curated datasets, tokenization standards, and instruction formats in the **Traversaal AI Urdu LLM Registry** ([traversaal-ai/urdu-llm-resources](https://github.com/traversaal-ai/urdu-llm-resources)).

### 1. Linguistic Preprocessing & Normalization
Urdu text requires specialized morphological normalization:
- **Aerab / Diacritics Stripping**: Removes Zabar, Zer, Pesh, Jazm, Tashdeed (`\u064B-\u065F\u0670\u06D6-\u06ED`).
- **Unicode Character Standardizer**:
  - Arabic Yeh (`ي`, `ى`), Yeh with Hamza (`ئ`) → Urdu Yeh (`ی`)
  - Arabic Kaf (`ك`) → Urdu Keheh (`ک`)
  - Ta Marbuta (`ة`), Arabic Heh (`ه`), Heh with Yeh (`ۂ`) → Urdu Choti Heh (`ہ`)
  - Retains aspirated Do-chashmi Heh (`ھ`) for proper phonetics (`دھان`, `کھاد`, `پھپھوندی`, `جھلسنا`).
- **Urdu Stopwords Filtering & N-Gram Indexing**: Filters functional markers (`سے`, `کا`, `کی`, `کے`, `کو`, `نے`, `میں`, `پر`, `ہے`, `ہیں`) while keeping domain entities.

### 2. Instruction Tuning Dataset Format
Instructions follow the standard Alpaca / Instruct schema:
```json
{
  "instruction": "فصلوں میں پھپھوندی (Fungal Diseases) کے اسباب اور تدارک کی تفصیل دیں۔",
  "input": "فصل کو پھپھوندی یا فنگس کی بیماری کیوں لگتی ہے اور اس کا علاج کیا ہے؟",
  "category": "disease_fungal",
  "intent": "fungal_disease",
  "response": "🔬 **پھپھوندی (Fungal Infection) کے اسباب اور حفاظتی تدابیر:...**"
}
```

---

## How to Train and Evaluate the Urdu Model

### 1. Train & Export Urdu NLP Classifier
Run the training pipeline:
```bash
python Practical_09_NLP_App/train_urdu_model.py
```
This will:
1. Ingest Urdu instruction datasets and domain knowledge.
2. Fit TF-IDF subword vectorizers and multinomial classifiers.
3. Validate intent recognition on sample test queries.
4. Export the serialized model to `Practical_09_NLP_App/urdu_ai_model.json`.

### 2. Interactive Testing via Python
```python
from Practical_09_NLP_App.nlp_chatbot import LocalFarmerChatbot

bot = LocalFarmerChatbot()
response = bot.ask("دھان کی فصل کے لیے کیا احتیاطی تدابیر ہیں؟", language="ur")
print(response["answer"])
```

### 3. Live API Endpoint (`/chat`)
Send HTTP POST requests to `http://localhost:8000/chat`:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "گندم کی فصل میں کھاد کا شیڈول کیا ہے؟", "language": "ur"}'
```
