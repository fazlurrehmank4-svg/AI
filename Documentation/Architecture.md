# CropGuard AI: System Architecture & Technical Specifications

---

## 1. End-to-End System Architecture

```mermaid
graph TD
    subgraph ClientLayer ["Mobile Client Layer (Flutter)"]
        UI[Flutter Mobile App]
        DASH[Dashboard & Gauges]
        CHAT_UI[Local AI Chatbot UI]
        PRED_UI[Crop Health Diagnosis]
    end

    subgraph APILayer ["FastAPI Backend Services (Python 3.11/3.14)"]
        API[FastAPI Gateway :8000]
        W_SVC[Weather Service Open-Meteo/OWM]
        PRED_ENG[CropGuard Multi-Model Engine]
        BOT_ENG[Local NLP Chatbot Engine]
        SUPA_SVC[Supabase Client & Auth Verifier]
    end

    subgraph IntelligenceLayer ["Core AI & ML Models"]
        OLS[Linear Regression Health Score - P06]
        TREE[Decision Tree / k-NN Classifier - P07]
        KM[K-Means Clustering - P08]
        FC[Forward Chaining Causes & Precautions - P05]
        BC[Backward Chaining Explainability - P05]
        ASTAR[A* Remediation Planning - P03]
        HC[Hill Climbing Microclimate Optimizer - P04]
        TFIDF[TF-IDF + Cosine Knowledge Retrieval - P09]
    end

    subgraph DataLayer ["Data & Storage Layer"]
        KB[(Kaggle Agricultural KB JSON)]
        SUPA_DB[(Supabase PostgreSQL + RLS)]
        AUTH[Supabase JWT Authentication]
    end

    UI -->|REST JSON| API
    API --> W_SVC
    API --> PRED_ENG
    API --> BOT_ENG
    API --> SUPA_SVC

    PRED_ENG --> OLS
    PRED_ENG --> TREE
    PRED_ENG --> KM
    PRED_ENG --> FC
    PRED_ENG --> BC

    BOT_ENG --> TFIDF
    BOT_ENG --> BC
    BOT_ENG --> KB

    SUPA_SVC --> SUPA_DB
    UI -->|Auth Tokens| AUTH
```

---

## 2. Multi-Model AI Prediction Pipeline

When a prediction is requested for a given crop and location:
1. **Weather Ingestion:** Real-time sensor values (temperature, relative humidity, precipitation, wind speed) are retrieved via the pluggable `WeatherService` (Open-Meteo / OpenWeatherMap).
2. **Feature Preprocessing:** Features are mapped into continuous normalized tensors for regression and classification, and discretized into proposition facts for expert rules.
3. **Continuous Prediction:** Practical 06 (Multiple Linear Regression) calculates the exact `crop_health_score` (0.0 to 100.0).
4. **Categorical Risk Assessment:** Practical 07 (CART Decision Tree) assigns the operational risk tier: `Healthy`, `At Risk`, or `High Risk`.
5. **Agro-Climatic Zoning:** Practical 08 (K-Means Clustering) determines the micro-climate archetype (`Favorable Regime`, `Moderate Stress`, or `Critical Vulnerability`).
6. **Deductive Etiology:** Practical 05 (Forward Chaining) fires domain rules to discover primary contributing causes and synthesize prioritized precautions.
7. **Transparent Explainability:** Practical 05 (Backward Chaining) tests why the primary risk condition was declared and outputs a human-readable justification string.

---

## 3. Local NLP Farmer Chatbot Architecture (Zero External LLMs)

```mermaid
flowchart TD
    Q[Farmer Query] --> NORM[Text Cleaning & Synonym Normalization]
    NORM --> STOP[Tokenization & Stopword Filtering]
    STOP --> ENT[Crop Entity Recognition & Intent Tagging]
    ENT --> CONTEXT{Active Prediction Context Available?}
    
    CONTEXT -->|Yes & Query is contextual| SYNTH[Synthesize Response with Active Crop & Diagnosis]
    CONTEXT -->|No or General Query| SIM[TF-IDF Vectorizer + Cosine Similarity Match]
    
    SIM --> THRESH{Cosine Similarity >= 0.22?}
    THRESH -->|Yes| RET[Retrieve Matched Agricultural Knowledge]
    THRESH -->|No| SAFE[Emit Transparent Educational Advisory & Supported Topics]
    
    SYNTH --> OUT[Deliver Explainable Response with Confidence Score]
    RET --> OUT
    SAFE --> OUT
```

---

## 4. Supabase Database & Security Architecture

- **PostgreSQL Database Tables:**
  - `profiles`: Farmer personal records, geographical location, primary cultivated crops.
  - `prediction_history`: Structured logs of every prediction (weather telemetry, continuous score, risk status, causes, precautions, timestamp).
  - `chat_history`: Conversation logs stored securely.
  - `crop_knowledge`: Public domain reference agronomic envelopes.
- **Row Level Security (RLS):**
  - All farmer tables enforce `auth.uid() = user_id`. No farmer can view, alter, or delete another farmer's historical records.
  - Client connections operate strictly with the public anonymous key (`SUPABASE_ANON_KEY`); administrative service-role keys are prohibited in client source code.
