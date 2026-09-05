# Practical 09: Domain-Specific Agricultural NLP Chatbot (Zero LLMs)

---

## 1. What Is It?
Practical 09 implements a 100% local, domain-specific **Natural Language Processing (NLP) Conversational Assistant** for agricultural decision support that runs entirely without external Large Language Models or paid third-party APIs (no OpenAI, Gemini, Claude, DeepSeek, or Groq).

## 2. Why Is It Used?
Rural agricultural extension tools require deterministic reliability, offline operability, zero external API token costs, data privacy, and zero tolerance for statistical hallucination. Grounding chatbot answers in calibrated Kaggle knowledge and formal reasoning engines delivers explainable and trustworthy farmer advisory.

## 3. How Does It Work?
The chatbot processes questions through a multi-tiered pipeline:
```
Farmer Question
      ↓
Text Normalization (lowercasing, punctuation stripping, synonym mapping)
      ↓
Tokenization & Stopword Filtering
      ↓
Intent Classification & Crop Entity Recognition
      ↓
Context-Aware Routing (detects active prediction state or backward-chaining 'Why' questions)
      ↓
TF-IDF Vectorization + Cosine Similarity Match against Kaggle knowledge base
      ↓
Reasoning Engine Integration (fires Backward Chaining for root cause justification)
      ↓
Confidence Scoring & Fallback Protection (conservative advisory if similarity < threshold)
```

## 4. Inputs & Outputs
- **Input:** Farmer question string, optional active crop entity, optional current prediction context object.
- **Output:** Structured response dictionary containing `answer`, `confidence`, `matched_topic`, `category`, and `reasoning_summary`.

## 5. Time & Space Complexity
- **Time Complexity:** $\mathcal{O}(V \cdot M)$ where $V$ is vocabulary size and $M$ is corpus documents. Retrieval executes in $< 2$ milliseconds.
- **Space Complexity:** $\mathcal{O}(V \cdot M)$ for sparse TF-IDF matrix representation.

## 6. Project Connection
Directly powers the **CropGuard AI Assistant** screen in Flutter and the `/chat` POST endpoint in the FastAPI backend (`Backend/routes/chat.py`).

## 7. Limitations
Cannot generate open-ended fictional dialogue outside of agriculture; intentionally restricted to supported agricultural and meteorological concepts to protect farmers from unsafe chemical or agronomic recommendations.

## 8. Runnable Command
```bash
python Practical_09_NLP_App/nlp_chatbot.py
```
