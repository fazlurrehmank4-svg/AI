# Abstract: CropGuard AI (Weather-Based Crop Health Predictor)

**Project Title:** CropGuard AI: Weather-Based Crop Health Predictor  
**Domain:** Artificial Intelligence, Machine Learning, Agro-Meteorology, Expert Systems  
**Authors:** College AI Project Team  

---

### Abstract
Smallholder farmers and agricultural producers face severe yield volatilization driven by volatile micro-climatic shifts, unpredicted humidity spikes, and rapid foliar pathogen germination. While modern Large Language Model (LLM) APIs have popularized conversational assistance, their deployment in rural agronomy is severely undermined by statistical hallucinations, recurring API token fees, internet latency, and lack of deterministic biological grounding.

This project introduces **CropGuard AI**, a full-stack, domain-specific agricultural decision support system designed as an academic capstone and practical field tool. CropGuard AI ingests real-time meteorological observations (temperature, relative humidity, precipitation, wind velocity) from WMO-calibrated weather stations and evaluates crop health through a multi-model intelligence pipeline. 

The architecture unifies the core curriculum of the first nine Artificial Intelligence Laboratory Practicals into an integrated enterprise system:
1. **Exploratory Data Analysis & Preprocessing (P01):** Validates agronomic bounds across Kaggle agricultural datasets.
2. **State-Space Exploration (P02):** Explores disease evolution and recovery trajectories via independent Breadth-First (BFS) and Depth-First Search (DFS).
3. **Informed Remediation Search (P03):** Employs Greedy Best-First Search and admissible A* search ($f(n) = g(n) + h(n)$) to plan the lowest-cost sequence of corrective agricultural actions.
4. **Micro-Climate Local Optimization (P04):** Uses Steepest-Ascent and Random-Restart Hill Climbing to calculate optimal irrigation rates and shade-net coverage.
5. **Deductive Reasoning & Explainability (P05):** Leverages a formal Propositional Expert System executing Forward Chaining for root cause discovery and Backward Chaining to answer *"Why did the AI reach this diagnosis?"*
6. **Continuous Prediction (P06):** Applies multiple Linear Regression to predict a continuous Crop Health Score (0-100).
7. **Operational Risk Categorization (P07):** Benchmarks k-Nearest Neighbors ($k=5$) and CART Decision Trees to classify status into `Healthy`, `At Risk`, or `High Risk`.
8. **Agro-Ecological Zoning (P08):** Applies unsupervised K-Means clustering to discover latent microclimate stress regimes.
9. **Local Agricultural NLP Chatbot (P09):** Implements an on-premise conversational assistant using TF-IDF vectorization, cosine similarity retrieval, and rule-based backward chaining without relying on any external LLM APIs (OpenAI, Gemini, Claude, or DeepSeek).

The system features a **FastAPI** Python backend, **Supabase PostgreSQL** authentication with strict Row Level Security (RLS) guaranteeing user-level isolation, and a modern cross-platform **Flutter** mobile application tailored for Android devices. Automated test suites confirm 100% test passing rates across backend endpoints, machine learning pipelines, and mobile widgets, fulfilling both rigorous viva defense standards and scalable software engineering practices.
