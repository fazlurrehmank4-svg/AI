# CropGuard AI: Weather-Based Crop Health Predictor

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Flutter-3.47+-02569B.svg?style=flat&logo=flutter)](https://flutter.dev)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-3776AB.svg?style=flat&logo=python)](https://python.org)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL%20RLS-3ECF8E.svg?style=flat&logo=supabase)](https://supabase.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Pipeline-F7931E.svg?style=flat&logo=scikit-learn)](https://scikit-learn.org)
[![Tests](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen.svg?style=flat)](#testing--verification)

> **A production-grade, college AI capstone project integrating 10 Artificial Intelligence Laboratory Practicals into an explainable agricultural decision support system with a Python FastAPI backend, Supabase PostgreSQL with Row Level Security, a 100% local NLP chatbot (zero external LLM APIs), and a modern Flutter mobile application.**

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Core Architecture](#core-architecture)
3. [The 10 AI Lab Practicals](#the-10-ai-lab-practicals)
4. [Custom Local Farmer Chatbot (Zero External LLMs)](#custom-local-farmer-chatbot-zero-external-llms)
5. [Machine Learning Pipeline & Evaluation](#machine-learning-pipeline--evaluation)
6. [Supabase Database & Row Level Security (RLS)](#supabase-database--row-level-security-rls)
7. [Security Architecture](#security-architecture)
8. [Flutter Mobile Application & UI Screens](#flutter-mobile-application--ui-screens)
9. [FastAPI Backend Endpoints](#fastapi-backend-endpoints)
10. [Quick Start & Setup Instructions](#quick-start--setup-instructions)
11. [Testing & Verification](#testing--verification)
12. [Android Release APK Build](#android-release-apk-build)
13. [Deployment (Render & Docker)](#deployment-render--docker)
14. [Academic Viva Defense & Documentation](#academic-viva-defense--documentation)
15. [Scientific Disclaimer & Limitations](#scientific-disclaimer--limitations)

---

## Project Overview

Agricultural yield vulnerability is predominantly governed by micro-meteorological shifts (high relative humidity, torrential rainfall, severe thermal anomalies). Smallholder farmers frequently lack timely, deterministic advice, while commercial generative AI chatbots suffer from hallucinations, high token pricing, and data privacy leaks.

**CropGuard AI** solves this through a multi-model, domain-specific architecture:
- **Live Meteorological Telemetry:** Open-Meteo real-time station data (zero API keys required) with OpenWeatherMap fallback.
- **Continuous Health Scoring:** Multiple Linear Regression ($R^2 = 0.7313$) predicting a continuous Crop Health Score ($0.0 \le y \le 100.0$).
- **Operational Risk Categorization:** CART Decision Tree (87.7% accuracy) & k-NN (88.3% accuracy) classifying risk into `Healthy`, `At Risk`, or `High Risk`.
- **Agro-Climatic Zoning:** Unsupervised K-Means clustering ($k=3$) identifying latent environmental stress zones.
- **Deductive Etiology & Explainability:** Propositional Expert System executing Forward Chaining for root cause discovery and Backward Chaining for XAI proofs.
- **Local Domain-Specific NLP Chatbot:** TF-IDF vectorizer + Cosine Similarity matching over structured Kaggle agricultural knowledge (100% local on-premise execution, zero OpenAI/Gemini/Claude API calls).
- **Enterprise Cloud Security:** Supabase PostgreSQL with strict Row Level Security (RLS) policies guaranteeing total user-level data isolation.

---

## Core Architecture

```
                 ┌──────────────────────────────────────┐
                 │       Flutter Mobile Client          │
                 │  - Dashboard & Health Gauges         │
                 │  - Live Weather Telemetry            │
                 │  - Crop Health Predictions           │
                 │  - Causes, Precautions & XAI Trace   │
                 │  - Local AI Farmer Chatbot Screen    │
                 └──────────────────┬───────────────────┘
                                    │  REST JSON
                                    ▼
                 ┌──────────────────────────────────────┐
                 │       FastAPI Backend (:8000)        │
                 │  - CORS Middleware & Safe Errors     │
                 │  - Asynchronous Route Dispatchers    │
                 │  - Pydantic Schema Validation        │
                 └──────┬───────────┬───────────┬───────┘
                        │           │           │
          ┌─────────────┘           │           └─────────────┐
          ▼                         ▼                         ▼
   ┌─────────────┐           ┌─────────────┐           ┌──────────────┐
   │ Weather API │           │  ML Models  │           │  Local NLP   │
   │ Open-Meteo  │           │ Regression  │           │   Chatbot    │
   │ OpenWeather │           │ k-NN & CART │           │ Kaggle Data  │
   │ Fallback    │           │ K-Means     │           │ TF-IDF + Sim │
   └─────────────┘           └──────┬──────┘           └──────┬───────┘
                                    │                         │
                                    ▼                         ▼
                             ┌───────────────────────────────────┐
                             │    Reasoning Engine (P05)         │
                             │  - Forward Chaining (Causes)      │
                             │  - Backward Chaining (XAI Proof)  │
                             └──────────────────┬────────────────┘
                                                │
                                                ▼
                                     ┌─────────────────────┐
                                     │   Supabase Cloud    │
                                     │  - Auth (JWT)       │
                                     │  - PostgreSQL DB    │
                                     │  - RLS Isolation    │
                                     └─────────────────────┘
```

---

## The 10 AI Lab Practicals

Every practical exists as an independently runnable academic script and contributes directly to the integrated system:

| Directory | Practical Focus | Implementation Highlights | Runnable Command |
| :--- | :--- | :--- | :--- |
| `Practical_01_Python_Environment` | Data Preprocessing & EDA | Pandas, NumPy, Matplotlib 4-panel correlation visual | `python Practical_01_Python_Environment/main.py` |
| `Practical_02_BFS_DFS` | Uninformed Graph Search | Independent BFS (FIFO) & DFS (LIFO) state exploration | `python Practical_02_BFS_DFS/bfs_dfs.py` |
| `Practical_03_GBFS_AStar` | Informed Heuristic Search | Greedy Best-First & A* ($f=g+h$) remediation cost minimization | `python Practical_03_GBFS_AStar/gbfs_astar.py` |
| `Practical_04_Local_Search` | Local Search Optimization | Steepest-Ascent & Random-Restart Hill Climbing (irrigation & shade) | `python Practical_04_Local_Search/hill_climbing.py` |
| `Practical_05_Reasoning` | Expert Reasoning Engine | Forward Chaining root causes & Backward Chaining explainability | `python Practical_05_Reasoning/reasoning_engine.py` |
| `Practical_06_Regression` | Continuous Prediction | Linear Regression ($R^2=0.7313$, $\text{MAE}=12.42$, $\text{RMSE}=17.08$) | `python Practical_06_Regression/regression_model.py` |
| `Practical_07_Classification` | Supervised Classification | Decision Tree (87.7% acc) & k-NN (88.3% acc) risk tiers | `python Practical_07_Classification/classification_models.py` |
| `Practical_08_Clustering` | Unsupervised Clustering | K-Means ($k=3$) micro-climate stress zone discovery | `python Practical_08_Clustering/clustering_model.py` |
| `Practical_09_NLP_App` | Domain-Specific NLP | Local TF-IDF + Cosine similarity assistant (Zero external LLMs) | `python Practical_09_NLP_App/nlp_chatbot.py` |
| `Practical_10_Mini_Project` | Integrated Application | Complete end-to-end multi-tier pipeline execution | `python Practical_10_Mini_Project/main.py` |

---

## Custom Local Farmer Chatbot (Zero External LLMs)

CropGuard AI **strictly adheres** to the mandate of avoiding external commercial LLM APIs (no OpenAI, Gemini, Claude, DeepSeek, or Groq).

### NLP Pipeline
```
Farmer Question 
      ↓
Text Normalization (lowercasing, punctuation stripping, synonym mapping)
      ↓
Tokenization & Stopword Filtering
      ↓
Crop Entity Recognition & Intent Classification
      ↓
Context Injection (incorporates active crop & prediction diagnosis)
      ↓
TF-IDF Vectorization & Cosine Similarity over Kaggle Agricultural Knowledge
      ↓
Backward Chaining Execution (answers "Why did you say risk is high?")
      ↓
Confidence Scoring & Fallback Protection (similarity < 0.22 triggers safe educational guidance)
```

### Sample Interactions
- **User:** *"What is the best temperature for wheat?"*  
  **CropGuard AI:** *"The optimal temperature envelope for Wheat is between 15°C and 25°C. Temperatures exceeding 30°C trigger terminal heat stress."*
- **User:** *"Why are my leaves turning yellow?"*  
  **CropGuard AI:** *"Yellowing leaves typically stem from: 1) Nitrogen deficiency, 2) Waterlogged root zones, or 3) Viral/root-rot infections."*
- **User:** *"What should I do?"* *(with active Tomato High Risk prediction)*  
  **CropGuard AI:** *"Your Tomato is assessed at High Risk (Score: 42/100). Key Cause: High canopy humidity. Recommended Action: Improve airflow, prune dense foliage, and apply copper fungicide."*
- **User:** *"Why did you say fungal risk is high?"*  
  **CropGuard AI:** *"Verified 'fungal_disease_risk_high' via RULE_FUNGAL_HIGH. Required conditions ['humidity_high', 'rainfall_high'] are satisfied by current observations."*

---

## Machine Learning Pipeline & Evaluation

| Model | Target Task | Primary Metrics | Artifact Path |
| :--- | :--- | :--- | :--- |
| **Multiple Linear Regression** | Continuous Health Score ($0-100$) | $R^2 = 0.7313$, $\text{MAE} = 12.42$, $\text{RMSE} = 17.08$ | `Backend/ai/saved_models/linear_regression.joblib` |
| **k-Nearest Neighbors ($k=5$)** | Categorical Risk Status | Accuracy = 88.33%, Macro F1 = 0.7587 | `Backend/ai/saved_models/knn_model.joblib` |
| **Decision Tree (CART, max_depth=6)** | Categorical Risk Status | Accuracy = 87.71%, Macro F1 = 0.7310 | `Backend/ai/saved_models/decision_tree_model.joblib` |
| **K-Means Clustering ($k=3$)** | Agro-Climatic Zoning | Silhouette Score = 0.2970, Inertia = 6123.13 | `Backend/ai/saved_models/kmeans_model.joblib` |

---

## Supabase Database & Row Level Security (RLS)

- **Hosted URL:** `https://tspdpkyhszrebrclsefz.supabase.co`
- **Tables:** `profiles`, `prediction_history`, `chat_history`, `crop_knowledge`.
- **Row Level Security Active:** YES.
- **User Isolation:** `auth.uid() = user_id` strictly enforced on all farmer tables.
- **Migration Scripts:** Located in `Supabase/schema.sql` and `Supabase/policies.sql`.

---

## Security Architecture

1. **Environment Variables:** All keys loaded via `.env` (`.env.example` provided). Zero secrets in Git.
2. **Client-Side Safety:** No `service_role` keys or private credentials embedded in Flutter.
3. **Pydantic Validation:** All API inputs type-checked with biological bounds enforcement.
4. **Safe Error Masking:** Production exceptions return sanitized JSON without stack traces.
5. **CORS:** Origin filtering enabled.

---

## Flutter Mobile Application & UI Screens

Built with **Flutter 3.47 (channel stable, Dart 3.13)**. Features custom agricultural design system (`theme.dart`) and original vector logo (`CropGuardLogo`).

### Screen Directory
1. **Splash Screen:** Animated brand presentation with initialization routing.
2. **Login Screen:** Email/password authentication, Supabase integration, Guest Mode.
3. **Sign Up Screen:** Farmer profile and farm district registration.
4. **Home Dashboard:** Farmer greeting, active crop selector, weather card, health gauge, quick actions.
5. **Crop Selection:** Grid of 8 cultivars with agronomic envelopes and emojis.
6. **Weather Telemetry:** District search, live sensors (temp, humidity, rain, wind, pressure).
7. **Crop Health Prediction:** Comprehensive multi-model analysis, health gauge, risk badge.
8. **Causes Screen:** Deep-dive into specific agronomic stress triggers.
9. **Precautions Screen:** Actionable cultural and chemical management checklist.
10. **Explanation Screen:** Backward Chaining reasoning trace explaining "Why this prediction?".
11. **Farmer Chatbot Screen:** Interactive conversational UI with suggested question chips.
12. **Prediction History:** Chronological prediction log with status badges and detail inspection.
13. **Profile Screen:** Farmer account details, primary crops, RLS verification.
14. **Settings Screen:** Configurable backend URL selector (`10.0.2.2:8000`, `127.0.0.1:8000`, cloud Render).
15. **About Screen:** Academic credits, 10 practicals mapping, scientific disclaimer.

---

## FastAPI Backend Endpoints

| Method | Route | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health status and active AI component manifest |
| `GET` | `/weather` | Real-time weather by city name or coordinates |
| `POST` | `/predict` | Full multi-model prediction + Forward/Backward Chaining |
| `POST` | `/chat` | Domain-specific local NLP query answering |
| `GET` | `/history` | User-isolated prediction history logs |
| `GET` | `/profile` | Farmer account profile retrieval |

---

## Quick Start & Setup Instructions

### 1. Prerequisites
- Python 3.11+ or 3.14+
- Flutter 3.19+ or 3.47+
- Git

### 2. Clone Repository
```bash
git clone https://github.com/fazlurrehmank4-svg/AI.git
cd AI
```

### 3. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env

# Generate dataset & train models
python Data/build_dataset.py
python Practical_06_Regression/regression_model.py
python Practical_07_Classification/classification_models.py
python Practical_08_Clustering/clustering_model.py

# Start FastAPI backend
uvicorn Backend.app:app --reload --port 8000
```
Interactive docs available at: `http://localhost:8000/docs`.

### 4. Flutter Setup
```bash
cd Flutter_App/weather_crop_health_app
flutter pub get
flutter run
```

---

## Testing & Verification

Run the automated test suites:
```bash
# Backend & AI test suite (10 tests)
pytest Backend/tests/ -v

# Flutter widget & unit test suite (5 tests)
cd Flutter_App/weather_crop_health_app
flutter test
```
**Results:** 100% tests passing across all suites.

---

## Android Release APK Build

To generate the production Android APK:
```bash
# Automated Windows batch script
.\build_apk.bat

# Or manually via Flutter CLI:
cd Flutter_App/weather_crop_health_app
flutter build apk --release
```
The output APK is generated at:
`Flutter_App/weather_crop_health_app/build/app/outputs/flutter-apk/app-release.apk`

---

## Deployment (Render & Docker)

1. **Docker Container:**
   ```bash
   docker build -t cropguard-ai .
   docker run -p 8000:8000 cropguard-ai
   ```
2. **Render Cloud Deployment:**
   - Link the GitHub repository: `https://github.com/fazlurrehmank4-svg/AI`.
   - Render automatically reads `render.yaml` and deploys the FastAPI backend on Python 3.11.

---

## Academic Viva Defense & Documentation

Comprehensive documentation files are located in `Documentation/`:
- **`Project_Report.md`**: Complete college-submission-grade project report.
- **`Abstract.md`**: Formal academic abstract.
- **`Architecture.md`**: Mermaid architecture flowcharts.
- **`AI_Algorithms.md`**: Mathematical equations and complexity proofs.
- **`API_Documentation.md`**: REST API endpoints specification.
- **`Security.md`**: Defense-in-depth security governance.
- **`Testing.md`**: Automated test reports.
- **`Viva_Questions.md`**: **105 Master Viva Questions and Answers** covering all practicals, algorithms, and architectures.

---

## Scientific Disclaimer & Limitations

> [!NOTE]
> **Educational Decision-Support Disclaimer:** CropGuard AI is an educational decision-support tool. Predictions are probabilistic assessments derived from meteorological indicators and biological knowledge envelopes. The system does not constitute an unconditional guarantee or a replacement for direct field inspection by certified agricultural extension agronomists.

---

## License
MIT License. Free for academic, educational, and open-source agricultural development.
