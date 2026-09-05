# Academic Project Report: CropGuard AI (Weather-Based Crop Health Predictor)

**Academic Year:** 2025–2026  
**Degree:** Bachelor of Technology / Bachelor of Engineering in Computer Science & Artificial Intelligence  
**Course:** Artificial Intelligence Laboratory & Capstone Mini-Project  
**Repository:** [https://github.com/fazlurrehmank4-svg/AI](https://github.com/fazlurrehmank4-svg/AI)  
**Supabase Instance:** `https://tspdpkyhszrebrclsefz.supabase.co`  

---

## Executive Summary

Agricultural productivity in agrarian economies faces persistent volatility due to micro-climatic disruptions, localized humidity surges, thermal anomalies, and rapid spore germination. Smallholder farmers often lack access to timely, localized, and scientific diagnostic advice.

**CropGuard AI** is a comprehensive, production-grade agricultural decision-support application built to bridge this gap. Rather than functioning as a synthetic demo or relying on third-party Large Language Model APIs (which introduce hallucinations, internet dependencies, and high recurring API token costs), CropGuard AI implements a robust, 100% local, explainable AI architecture that unifies the first nine Artificial Intelligence Laboratory practicals into an end-to-end operational software product.

---

## Chapter 1: Introduction & Problem Statement

### 1.1 Problem Definition
Crop vulnerability is heavily driven by meteorology. For instance:
- Relative humidity exceeding 80% accompanied by moderate temperatures triggers fungal pathogens (e.g. Rice Blast, Early Blight).
- Excessive rainfall coupled with poor soil percolation produces root hypoxia and water mold diseases.
- High ambient temperatures during grain-filling phases cause terminal heat shock in wheat.

Current advisory tools are either static brochures or generic LLM chatbots that lack deterministic biological knowledge and risk hallucinatory chemical recommendations.

### 1.2 Project Objectives
1. Ingest real-time meteorological observations (temperature, relative humidity, precipitation, wind speed) from live weather stations.
2. Clean and structure Kaggle agricultural datasets into deterministic agronomic envelopes.
3. Compute a continuous Crop Health Score (0–100) using Multiple Linear Regression.
4. Classify operational health tiers (`Healthy`, `At Risk`, `High Risk`) via CART Decision Trees and k-NN.
5. Cluster macro-climatic environments using unsupervised K-Means clustering.
6. Deduce root causes and prioritized precautions via a formal Forward Chaining Expert System.
7. Deliver explainable AI (XAI) proofs via Backward Chaining.
8. Implement an on-premise local NLP chatbot using TF-IDF vectorization and cosine similarity (zero external LLMs).
9. Integrate Supabase PostgreSQL authentication and database storage with strict Row Level Security (RLS).
10. Deliver a high-polish, cross-platform mobile application in Flutter suitable for Android deployment.

---

## Chapter 2: Comprehensive AI Practicals Integration

CropGuard AI explicitly embodies the college Artificial Intelligence laboratory curriculum:

| Practical Code | Classical AI Algorithm | Project Functional Role |
| :--- | :--- | :--- |
| **Practical 01** | NumPy, Pandas, Matplotlib | Data preprocessing, cleaning, missing-value audit, and multivariate correlation plots. |
| **Practical 02** | Breadth-First Search (BFS) & Depth-First Search (DFS) | State-space exploration of crop degradation pathways and recovery actions. |
| **Practical 03** | Greedy Best-First & A* Search ($f = g + h$) | Finding the mathematically optimal, minimum-cost sequence of agronomic remediation actions. |
| **Practical 04** | Steepest-Ascent & Random-Restart Hill Climbing | Local search optimization of field irrigation volume and shade-net percentage. |
| **Practical 05** | Forward & Backward Chaining Propositional Inference | Forward: Root cause & precaution deduction; Backward: Explainable AI proof generation. |
| **Practical 06** | Multiple Linear Regression ($R^2 = 0.7313$) | Continuous Crop Health Score calculation ($0.0 \le y \le 100.0$). |
| **Practical 07** | CART Decision Tree (depth=6) & k-NN ($k=5$) | Multiclass operational risk categorization (`Healthy`, `At Risk`, `High Risk`). |
| **Practical 08** | Unsupervised K-Means Clustering ($k=3$) | Partitioning agricultural observations into distinct agro-climatic stress regimes. |
| **Practical 09** | Local Domain-Specific NLP Knowledge Retrieval | Conversational farmer assistant using TF-IDF and cosine similarity (zero external LLM APIs). |
| **Practical 10** | Integrated Enterprise Mini-Project | Full-stack orchestration connecting weather, ML models, rules, database, and Flutter. |

---

## Chapter 3: Data Engineering & Agronomic Knowledge Base

### 3.1 Dataset Calibration
Dataset records were calibrated using Kaggle Agricultural datasets (Crop Recommendation & Weather Impact) covering eight core agronomic cultivars:
- **Cereals:** Wheat, Rice, Maize
- **Commercial & Cash Crops:** Cotton, Sugarcane
- **Horticulture & Tubers:** Tomato, Potato
- **Pulses:** Chickpea

### 3.2 Knowledge Base Schema (`crop_knowledge.json`)
Structured biological thresholds include:
- `temp_optimal`: `[min_temp, max_temp]` in °C.
- `humidity_optimal`: `[min_humidity, max_humidity]` in % RH.
- `rainfall_optimal`: `[min_rainfall, max_rainfall]` in mm.
- `soil_type` and `water_requirement`.
- Susceptible pathologies with symptoms, triggers, causes, and approved cultural precautions.

---

## Chapter 4: Architecture & Security Engineering

### 4.1 Backend Services
Built with **FastAPI** running on Uvicorn:
- Asynchronous non-blocking route dispatching.
- CORS middleware with configured origin filtering.
- Safe global exception handler preventing internal stack trace disclosure.
- Strict Pydantic validation on all endpoints.

### 4.2 Supabase Database & Row Level Security (RLS)
- Hosted PostgreSQL instance: `https://tspdpkyhszrebrclsefz.supabase.co`.
- Tables: `profiles`, `prediction_history`, `chat_history`, `crop_knowledge`.
- RLS Policy Rule:
  ```sql
  CREATE POLICY "Users can view own prediction history"
      ON public.prediction_history
      FOR SELECT
      USING (auth.uid() = user_id);
  ```
- Guaranteed zero cross-farmer data visibility.

---

## Chapter 5: Mobile Application & UI/UX Design System

Developed in **Flutter 3.47 (Dart 3.13)**:
- **Design System:** `theme.dart` featuring an organic agricultural palette (Emerald Green `#1B5E20`, Fresh Leaf `#4CAF50`, Mint `#E8F5E9`), accessible typography, and card tokens.
- **Original Brand Logo:** Custom vector painter integrating Leaf + Sun/Weather + Digital AI Nodes.
- **16 Screen Workflows:**
  1. Splash Screen
  2. Login Screen
  3. Sign Up Screen
  4. Home Dashboard
  5. Crop Selection
  6. Location & Weather Telemetry
  7. Crop Health Prediction
  8. Causes Breakdown
  9. Precautions Checklist
  10. AI Explanation (XAI Trace)
  11. Farmer Chatbot (CropGuard Assistant)
  12. Prediction History
  13. Profile
  14. Settings (Configurable backend URL)
  15. About Screen
  16. Navigation Drawer

---

## Chapter 6: Verification, Testing & Empirical Results

1. **Backend Integration Tests:** 10/10 tests passing on Pytest across `/health`, `/weather`, `/predict`, `/chat`, `/history`, and `/profile`.
2. **ML Model Benchmarks:**
   - Linear Regression: $R^2 = 0.7313$, $\text{MAE} = 12.42$, $\text{RMSE} = 17.08$.
   - k-NN ($k=5$): Accuracy = 88.33%, Macro F1 = 0.7587.
   - Decision Tree (depth=6): Accuracy = 87.71%, Macro F1 = 0.7310.
   - K-Means ($k=3$): Silhouette Score = 0.2970.
3. **Local NLP Chatbot Validation:** Successfully answered queries across crop envelopes, disease symptoms, weather impacts, backward chaining explanations, and safely rejected out-of-domain queries without hallucinating.
4. **Flutter UI Tests:** 5/5 tests passing cleanly verifying custom logo, health score gauge, risk badge, weather card, and crop model invariants.

---

## Chapter 7: Conclusion & Future Scope

### 7.1 Conclusion
CropGuard AI successfully demonstrates that classical and modern machine learning, expert systems, and lightweight local NLP can be unified into a production-grade, privacy-preserving, and explainable decision-support tool for smallholder farmers, eliminating reliance on costly and unpredictable external LLM APIs.

### 7.2 Future Scope
1. **Multispectral Satellite Telemetry:** Integrating Sentinel-2 NDVI vegetative index feeds.
2. **IoT In-Situ Sensors:** Connecting direct LoRaWAN soil moisture and NPK telemetry.
3. **Vernacular Voice Interface:** Integrating local offline speech-to-text models (e.g. Whisper-tiny) for illiterate rural producers.
