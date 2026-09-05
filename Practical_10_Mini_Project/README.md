# Practical 10: Complete Integrated AI Mini-Project (CropGuard AI)

---

## 1. What Is It?
Practical 10 is the holistic, end-to-end integration of all nine preceding Artificial Intelligence laboratory practicals into a unified, production-ready agricultural decision support system: **CropGuard AI: Weather-Based Crop Health Predictor**.

## 2. Integrated Architectural Architecture
```
                         ┌────────────────────────────────────────┐
                         │   1. Meteorological Observation        │
                         │   (Open-Meteo / Local Farm Station)    │
                         └──────────────────┬─────────────────────┘
                                            │
                                            ▼
                         ┌────────────────────────────────────────┐
                         │   2. Data Preprocessing & Validation   │
                         │   (Practical 01: Agronomic Bounds)     │
                         └──────────────────┬─────────────────────┘
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               ▼                            ▼                            ▼
┌─────────────────────────────┐ ┌───────────────────────────┐ ┌────────────────────────────┐
│ 3. Linear Regression (P06)  │ │ 4. Decision Tree / kNN    │ │ 5. K-Means Clustering     │
│ Continuous Health (0-100)   │ │ Classification (P07)      │ │ Microclimate Regime (P08) │
└──────────────┬──────────────┘ └─────────────┬─────────────┘ └─────────────┬──────────────┘
               │                              │                             │
               └──────────────────────────────┼─────────────────────────────┘
                                              │
                                              ▼
                         ┌────────────────────────────────────────┐
                         │   6. Forward Chaining Engine (P05)     │
                         │   Deduced Causes & Precautions         │
                         └──────────────────┬─────────────────────┘
                                            │
               ┌────────────────────────────┴────────────────────────────┐
               ▼                                                         ▼
┌─────────────────────────────┐                         ┌─────────────────────────────────┐
│ 7. Backward Chaining (P05)  │                         │ 8. Heuristic Planning Modules   │
│ Explainable Verification    │                         │ - A* Remediation Sequence (P03) │
│ "Why is this risk flagged?" │                         │ - Hill Climbing Tuning (P04)    │
│                             │                         │ - BFS/DFS State Search (P02)    │
└──────────────┬──────────────┘                         └─────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. Local Domain-Specific NLP Chatbot (Practical 09)             │
│ Context-Aware Farmer Advisory (Zero External LLM APIs)          │
└─────────────────────────────────────────────────────────────────┘
```

## 3. How Each Practical Contributes to Practical 10
1. **Practical 01:** Cleans, audits, and formats raw meteorological data into scaled continuous variables.
2. **Practical 02:** Models the crop health degradation graph and traces failure states using BFS/DFS.
3. **Practical 03:** Employs A* informed search to discover the lowest-cost sequence of agronomic remediation actions.
4. **Practical 04:** Optimizes irrigation rates and shade-net coverage via Hill Climbing to maximize crop comfort.
5. **Practical 05:** Generates root causes through Forward Chaining and provides explainability through Backward Chaining.
6. **Practical 06:** Computes the continuous numerical Crop Health Score (0-100).
7. **Practical 07:** Classifies operational health into `Healthy`, `At Risk`, or `High Risk`.
8. **Practical 08:** Discovers latent micro-climatic vulnerability zones via unsupervised clustering.
9. **Practical 09:** Delivers the interactive local NLP conversational assistant.

## 4. Execution Command
```bash
python Practical_10_Mini_Project/main.py
```
