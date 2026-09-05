# CropGuard AI: Comprehensive Academic Viva Questions & Answers (105 Questions)

This document serves as the master study guide and examination reference for defending the **CropGuard AI (Weather-Based Crop Health Predictor)** mini-project in college oral examinations and laboratory viva defense.

---

## Category 1: Overall System Architecture & Core Concept (Q1 - Q15)

#### Q1: What is the primary objective of the CropGuard AI project?
**Ans:** CropGuard AI is an agricultural decision-support system that predicts crop health, identifies disease risks, deduces root causes, and recommends actionable precautions by analyzing real-time weather telemetry and historical agronomic data.

#### Q2: Why is the application called a "decision-support system" rather than a replacement for agronomists?
**Ans:** Agricultural biology is complex and subject to unobserved soil and biotic variables. Calling it a decision-support system reinforces the scientifically responsible disclaimer that AI provides probabilistic guidance, not an unconditional legal or agronomic guarantee.

#### Q3: What technologies comprise the full-stack architecture?
**Ans:** 
- **Frontend:** Flutter (Dart) mobile application.
- **Backend:** FastAPI (Python 3.11/3.14).
- **Database & Auth:** Supabase PostgreSQL with Row Level Security (RLS).
- **Machine Learning:** Scikit-learn, NumPy, Pandas.
- **NLP & Chatbot:** Local TF-IDF vectorizer + Cosine Similarity + Rule-Based Reasoning Engine (Zero external LLMs).
- **Weather:** Open-Meteo API / OpenWeatherMap.

#### Q4: Why did you choose FastAPI over Flask or Django?
**Ans:** FastAPI supports native asynchronous execution (`async/await`), automatic OpenAPI/Swagger documentation generation, high throughput via Starlette/Uvicorn, and built-in type validation via Pydantic.

#### Q5: What was the main motivation for avoiding external LLM APIs (OpenAI, Gemini, Claude, DeepSeek) in the chatbot?
**Ans:** 
1. Deterministic safety: LLMs can hallucinate incorrect chemical remedies.
2. Cost: Third-party APIs incur recurring per-token fees unaffordable for smallholders.
3. Offline feasibility: Local NLP operates without expensive cloud infrastructure.
4. Privacy: Farmer questions remain on-premise.

#### Q6: How do the 9 AI practicals integrate into the single mini-project?
**Ans:** 
- P01: Cleans and preprocesses Kaggle agricultural data.
- P02: BFS/DFS explores disease escalation state spaces.
- P03: A* plans minimal-cost remediation sequences.
- P04: Hill Climbing optimizes irrigation and shade microclimate.
- P05: Forward/Backward chaining provides cause detection and explainability.
- P06: Linear regression computes continuous crop health score.
- P07: Decision tree/k-NN classifies risk status (`Healthy`, `At Risk`, `High Risk`).
- P08: K-Means clusters microclimate vulnerability zones.
- P09: Local NLP delivers the farmer conversational assistant.
- P10: Unifies all above modules into the end-to-end pipeline.

#### Q7: Does A* directly predict whether a crop has disease?
**Ans:** No. A* is an informed path-planning algorithm. It is used to discover the lowest-cost sequence of corrective agricultural treatments after a risk has been identified.

#### Q8: Where does the agricultural knowledge base originate?
**Ans:** Curated from benchmark Kaggle Agricultural Datasets (Crop Recommendation, Weather Impact) transformed into structured agronomic envelopes in `Data/knowledge_base/crop_knowledge.json`.

#### Q9: What crops are supported?
**Ans:** 8 major crops: Rice, Wheat, Maize, Cotton, Tomato, Potato, Sugarcane, and Chickpea.

#### Q10: How does the application handle offline mode?
**Ans:** It caches default baseline agricultural weather data and stores user predictions in local memory if Supabase or remote weather services are temporarily unreachable.

#### Q11: What is the Crop Health Score?
**Ans:** A continuous index from 0.0 to 100.0 representing the physiological vigor of the crop based on its deviation from optimal temperature, humidity, rainfall, and wind envelopes.

#### Q12: How is the risk level categorized?
**Ans:** 
- Health Score $\ge 75$: `Healthy` (Low Risk)
- Health Score $50 - 74.9$: `At Risk` (Moderate Risk)
- Health Score $< 50$: `High Risk` (High Risk)

#### Q13: What is the role of Supabase Auth?
**Ans:** Issues cryptographically signed JSON Web Tokens (JWT) for user signup, login, session persistence, and authorization.

#### Q14: How does the system achieve Explainable AI (XAI)?
**Ans:** Through Backward Chaining in Practical 05, which justifies diagnostic conclusions by tracing unsatisfied or satisfied antecedents back to verified sensor facts.

#### Q15: How is user data isolated?
**Ans:** Supabase Row Level Security (RLS) policies enforce `auth.uid() = user_id` on every query, preventing cross-tenant data access.

---

## Category 2: Practical 01: Python Environment & EDA (Q16 - Q23)

#### Q16: What is Practical 01?
**Ans:** Data loading, auditing, preprocessing, and multivariate correlation visualization using Python, NumPy, Pandas, and Matplotlib.

#### Q17: Why is Exploratory Data Analysis (EDA) necessary before machine learning?
**Ans:** It uncovers data skew, missing values, extreme outliers, and relationships between meteorological inputs and crop vigor.

#### Q18: What is Z-score normalization?
**Ans:** $z = \frac{x - \mu}{\sigma}$. It scales features to mean 0 and unit variance, preventing high-magnitude features (e.g. rainfall in mm) from dominating lower-magnitude ones (e.g. temperature in °C).

#### Q19: What visualizations were generated in Practical 01?
**Ans:** A 4-panel visual: 1) Health score histogram, 2) Temperature vs. Health score scatter, 3) Health status bar chart, 4) Humidity vs. Rainfall colormap scatter (`weather_crop_analysis.png`).

#### Q20: What is the time complexity of Practical 01?
**Ans:** $\mathcal{O}(N \times M)$ where $N$ is samples (2,400) and $M$ is features (13).

#### Q21: What did the missing value audit reveal?
**Ans:** Zero missing values across all 2,400 curated records.

#### Q22: What is the limitation of EDA?
**Ans:** It reveals historical correlations but cannot execute predictive inference on novel real-time observations.

#### Q23: How does Practical 01 link to the final project?
**Ans:** It establishes the normalized datasets and validation parameters used across Practicals 06, 07, 08, and the backend.

---

## Category 3: Practical 02: BFS & DFS Search (Q24 - Q31)

#### Q24: What is the purpose of Practical 02?
**Ans:** Demonstrates uninformed search algorithms (BFS and DFS) on an agricultural vulnerability state graph.

#### Q25: How does BFS operate in this project?
**Ans:** Uses a FIFO queue to explore state transitions level-by-level, guaranteeing the shortest path from a stressed state back to `Recovered_Healthy_Crop`.

#### Q26: How does DFS operate?
**Ans:** Uses a LIFO stack to traverse deeply along single risk branches, exposing worst-case disease escalation paths (e.g. `Severe_Foliar_Blight`).

#### Q27: What is the time complexity of BFS and DFS?
**Ans:** $\mathcal{O}(V + E)$, where $V$ is vertices (agricultural states) and $E$ is edges (transitions).

#### Q28: What is the space complexity difference between BFS and DFS?
**Ans:** BFS requires $\mathcal{O}(V)$ memory for the queue; DFS requires $\mathcal{O}(h)$ memory for the stack, where $h$ is maximum tree depth.

#### Q29: What is a major limitation of uninformed search?
**Ans:** It treats all transitions equally and cannot incorporate financial costs or heuristic distance estimates.

#### Q30: What was the shortest mitigation path found by BFS?
**Ans:** `Healthy_Crop` $\to$ `Moderate_Drought_Stress` $\to$ `Controlled_Drip_Irrigation` $\to$ `Recovered_Healthy_Crop` (3 steps).

#### Q31: How does Practical 02 connect to the final project?
**Ans:** It models discrete crop vulnerability state progressions for decision audit trails.

---

## Category 4: Practical 03: Informed Heuristic Search (GBFS & A*) (Q32 - Q40)

#### Q32: What is informed search?
**Ans:** Search strategies that use problem-specific heuristic knowledge $h(n)$ to guide exploration towards the goal efficiently.

#### Q33: What is the evaluation function of Greedy Best-First Search?
**Ans:** $f(n) = h(n)$. It expands the node that appears closest to the goal.

#### Q34: Why can GBFS find sub-optimal paths?
**Ans:** It ignores accrued path cost $g(n)$, making it vulnerable to deceptive local shortcuts that have higher total costs.

#### Q35: What is the evaluation function of A* search?
**Ans:** $f(n) = g(n) + h(n)$, summing actual path cost $g(n)$ and estimated remaining cost $h(n)$.

#### Q36: What does it mean for a heuristic to be "admissible"?
**Ans:** $h(n) \le h^*(n)$ for all $n$. It never overestimates the true minimal cost to reach the goal.

#### Q37: What does admissibility guarantee in A*?
**Ans:** Guaranteed discovery of the mathematically optimal, lowest-cost path on tree/graph searches.

#### Q38: What does consistency (monotonicity) mean for a heuristic?
**Ans:** $h(n) \le c(n, a, n') + h(n')$. The heuristic estimate cannot decrease along an edge by more than the edge cost.

#### Q39: What was the optimal remediation path found by A* in Practical 03?
**Ans:** `Severe_Fungal_Outbreak` $\to$ `Foliage_Canopy_Pruning` $\to$ `Aeration_Improvement` $\to$ `Optimal_Microclimate_Restored` with total cost = 37 units.

#### Q40: What is the project connection of Practical 03?
**Ans:** Powers the Remediation Cost Optimizer that selects the cheapest sequence of field actions to mitigate severe outbreaks.

---

## Category 5: Practical 04: Local Search & Hill Climbing (Q41 - Q48)

#### Q41: What is Hill Climbing?
**Ans:** An iterative local search algorithm that starts from an initial state and moves greedily in the direction of increasing objective function value.

#### Q42: What is the state representation in Practical 04?
**Ans:** A 2-tuple $(\text{irrigation\_mm}, \text{shade\_percent})$.

#### Q43: What is the objective function?
**Ans:** Crop Physiological Comfort Score (0 to 100), combining evapotranspiration compensation and thermal canopy moderation.

#### Q44: What are the primary drawbacks of simple Hill Climbing?
**Ans:** Getting trapped in local maxima, ridges, and plateaus.

#### Q45: How does Random-Restart Hill Climbing solve the local maximum problem?
**Ans:** By executing multiple restarts from uniformly randomized starting coordinates and recording the best global solution found.

#### Q46: What occurred in Experiment 1 vs Experiment 2 in Practical 04?
**Ans:** Starting near $(6.0, 12.0)$ converged to a local peak of 71.75/100; starting near $(20.0, 30.0)$ reached the global maximum of 99.88/100.

#### Q47: What is the time complexity of Hill Climbing?
**Ans:** $\mathcal{O}(K \times \text{neighborhood size})$ where $K$ is ascent steps until termination.

#### Q48: How does Practical 04 connect to the final project?
**Ans:** Computes continuous microclimate adjustments (irrigation volume and shade-net percentage) when farmers face heatwaves.

---

## Category 6: Practical 05: Reasoning Engine (Forward & Backward Chaining) (Q49 - Q58)

#### Q49: What is Forward Chaining?
**Ans:** A data-driven inference method that starts with known facts and applies Modus Ponens across rules to deduce new conclusions until a fixpoint is reached.

#### Q50: What is Backward Chaining?
**Ans:** A goal-driven inference method that starts with a target hypothesis and works backwards to verify if underlying evidence supports it.

#### Q51: How are facts extracted from weather observations?
**Ans:** By discretizing continuous values (e.g. humidity $\ge 78\%$ becomes `humidity_high`; temp $\ge 32^\circ\text{C}$ becomes `temperature_high`).

#### Q52: State an example rule from Practical 05.
**Ans:** 
`IF humidity_high AND rainfall_high THEN fungal_disease_risk_high`.

#### Q53: What causes and precautions are deduced from the fungal rule?
**Ans:** 
- **Causes:** Prolonged leaf wetness, dense vegetative cover, high humidity.
- **Precautions:** Thin lower canopy, suspend overhead sprinkling, apply copper bio-fungicide.

#### Q54: How does Backward Chaining provide Explainable AI (XAI)?
**Ans:** When asked *"Why is fungal risk high?"*, it evaluates the goal, identifies `RULE_FUNGAL_HIGH`, checks verified facts, and outputs a human-readable proof.

#### Q55: What happens when Backward Chaining queries an unproven goal?
**Ans:** It returns `False`, lists the missing required conditions, and explains why the goal could not be proven.

#### Q56: What is the time complexity of Forward Chaining?
**Ans:** $\mathcal{O}(R \times C)$ where $R$ is rules count and $C$ is conditions per rule.

#### Q57: How does Practical 05 prevent duplicate deductions?
**Ans:** By maintaining tracked rule execution lists and unique consequence sets.

#### Q58: How does Practical 05 connect to the final project?
**Ans:** Directly generates the Causes, Precautions, and AI Explanation in the mobile prediction screen and chatbot.

---

## Category 7: Practical 06: Linear Regression (Q59 - Q67)

#### Q59: What is Linear Regression?
**Ans:** A supervised learning method modeling the linear relationship between independent regressors and a continuous target variable.

#### Q60: What are the input features and target variable in Practical 06?
**Ans:** 
- **Inputs:** Temperature, humidity, rainfall, wind speed.
- **Target:** Continuous `crop_health_score` (0.0 to 100.0).

#### Q61: What was the $R^2$ score achieved by your Linear Regression model?
**Ans:** $R^2 = 0.7313$, meaning the model explains $\approx 73.1\%$ of the variance in crop health score from meteorological inputs.

#### Q62: What were the MAE and RMSE values?
**Ans:** $\text{MAE} = 12.42$ points, $\text{RMSE} = 17.08$ points.

#### Q63: What does the sign of regression coefficients indicate?
**Ans:** Positive coefficients indicate features positively correlating with health in the tested range; negative coefficients (e.g., wind speed: $-28.31$) indicate stress-inducing factors.

#### Q64: How are regression predictions constrained to realistic biological boundaries?
**Ans:** Predictions are clipped to the interval $[5.0, 98.0]$ using NumPy clip.

#### Q65: Why is feature scaling applied before Linear Regression?
**Ans:** To standardize feature scales so coefficients reflect relative importance without distortion from feature units.

#### Q66: What is the time complexity of training Linear Regression?
**Ans:** $\mathcal{O}(d^2 n + d^3)$ where $n$ is samples and $d$ is features.

#### Q67: How does Practical 06 connect to the final project?
**Ans:** Directly drives the animated circular health gauge on the Flutter dashboard.

---

## Category 8: Practical 07: k-NN & Decision Tree Classification (Q68 - Q77)

#### Q68: What is the classification task in Practical 07?
**Ans:** Categorizing agricultural health status into three multiclass categories: `Healthy`, `At Risk`, or `High Risk`.

#### Q69: What is k-Nearest Neighbors (k-NN)?
**Ans:** An instance-based non-parametric classifier that assigns a class by majority vote of its $k$ closest neighbors in Euclidean space.

#### Q70: What value of $k$ was selected and why?
**Ans:** $k = 5$. An odd number avoids tie votes in binary splits and balances bias-variance tradeoff.

#### Q71: What is a Decision Tree classifier?
**Ans:** A hierarchical model that recursively partitions the feature space into axis-aligned hyperplanes using impurity criteria.

#### Q72: What splitting criterion did you use for the Decision Tree?
**Ans:** Gini Impurity: $I_G = 1 - \sum p_i^2$.

#### Q73: Why did you set `max_depth = 6` on the Decision Tree?
**Ans:** To prevent overfitting on noisy weather variations and maintain high interpretability.

#### Q74: What accuracy did both models achieve?
**Ans:** 
- k-NN: 88.33% accuracy (Macro F1: 0.7587).
- Decision Tree: 87.71% accuracy (Macro F1: 0.7310).

#### Q75: Why evaluate Macro F1-score in addition to Accuracy?
**Ans:** Because agricultural risk classes can be imbalanced; Macro F1-score weights performance equally across all three classes.

#### Q76: What is a Confusion Matrix?
**Ans:** A cross-tabulation table displaying True Positives, True Negatives, False Positives, and False Negatives for each class.

#### Q77: How does Practical 07 connect to the final project?
**Ans:** Provides the categorical color-coded badge (`Healthy` - Green, `At Risk` - Orange, `High Risk` - Red) shown on all screens.

---

## Category 9: Practical 08: K-Means Clustering (Q78 - Q85)

#### Q78: What is K-Means Clustering?
**Ans:** An unsupervised learning algorithm that partitions $n$ unlabeled observations into $k$ clusters where each point belongs to the cluster with the nearest centroid.

#### Q79: What value of $k$ was chosen in Practical 08?
**Ans:** $k = 3$, corresponding to three natural environmental regimes: Favorable, Moderate Stress, and Critical Vulnerability.

#### Q80: What is the k-Means++ initialization algorithm?
**Ans:** A smart seeding method that chooses initial cluster centers far apart from each other, improving convergence speed and avoiding bad local minima.

#### Q81: What is Inertia in K-Means?
**Ans:** The within-cluster sum-of-squares distances: $\sum \|\mathbf{x} - \boldsymbol{\mu}_j\|^2$. Lower inertia indicates tighter clusters.

#### Q82: What is the Silhouette Score?
**Ans:** A metric measuring how similar an object is to its own cluster compared to other clusters, ranging from $-1$ to $+1$.

#### Q83: What did the cluster centroids reveal?
**Ans:**
- Cluster 0 (Favorable): Moderate temp ($21.4^\circ\text{C}$), balanced humidity ($62.5\%$), average health score 86.5/100.
- Cluster 1 (Critical): High wind ($41.0\text{ km/h}$), extreme dry air ($19.3\%$), average health score 17.0/100.
- Cluster 2 (Stress): Warm ($29.3^\circ\text{C}$), high humidity ($81.4\%$), high rain ($179.7\text{ mm}$), average health score 72.2/100.

#### Q84: What is a limitation of K-Means?
**Ans:** Assumes spherical clusters of equal variance and requires specifying $k$ in advance.

#### Q85: How does Practical 08 connect to the final project?
**Ans:** Generates the "Agro-Climatic Regime" tag displayed on the prediction cards.

---

## Category 10: Practical 09: Local NLP Farmer Chatbot (Q86 - Q96)

#### Q86: How does the local NLP chatbot process a user question?
**Ans:**
1. Text normalization: lowercasing, punctuation stripping, synonym mapping.
2. Tokenization & stopword removal.
3. Crop entity detection.
4. TF-IDF vectorization & Cosine Similarity matching against agricultural knowledge base.
5. Context injection (integrating active crop/prediction).
6. Backward chaining execution for "Why" questions.
7. Conservative confidence thresholding (fallback if score $< 0.22$).

#### Q87: What is TF-IDF?
**Ans:** Term Frequency-Inverse Document Frequency. Measures how important a word is to a document within a corpus, balancing word frequency with rarity across documents.

#### Q88: What is Cosine Similarity?
**Ans:** The cosine of the angle between two multi-dimensional vectors: $\frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$. It measures directional orientation rather than text length magnitude.

#### Q89: How does the chatbot handle variations in wording?
**Ans:** Synonym normalization maps phrases like *"humidity is too high"*, *"high moisture problem"*, and *"damp air"* to normalized tokens before TF-IDF vectorization.

#### Q90: How does the chatbot handle context-dependent questions like "What should I do?"?
**Ans:** It inspects the `current_prediction` payload. If active context exists, it extracts the crop, health score, primary causes, and top precautions, formulating an immediate tailored response.

#### Q91: How does the chatbot answer "Why did you say fungal risk is high?"?
**Ans:** It invokes the Practical 05 Backward Chaining engine, verifying the active sensor facts against `RULE_FUNGAL_HIGH` to generate a rule-trace justification.

#### Q92: What happens if a farmer asks an out-of-domain question (e.g., "Recommend crypto stocks")?
**Ans:** The cosine similarity falls below 0.22. The system rejects the question, states its knowledge limitations, and lists supported agricultural topics without hallucinating.

#### Q93: Does the chatbot use any external LLMs (OpenAI, Gemini, Claude)?
**Ans:** No. It runs 100% locally via Python scikit-learn, TF-IDF, cosine similarity, and expert rule reasoning.

#### Q94: What is the retrieval latency of the local chatbot?
**Ans:** Under 5 milliseconds per query on local CPU.

#### Q95: What are the main limitations of this local chatbot?
**Ans:** It cannot generate arbitrary conversational creative prose; it is intentionally constrained to verified agronomic topics to ensure safety.

#### Q96: How does Practical 09 connect to the final project?
**Ans:** Directly powers the `/chat` POST endpoint and the interactive CropGuard AI Assistant screen in Flutter.

---

## Category 11: Supabase, Security, Flutter & Deployment (Q97 - Q105)

#### Q97: How is Supabase Row Level Security (RLS) configured?
**Ans:** RLS is enabled on all tables (`profiles`, `prediction_history`, `chat_history`, `crop_knowledge`). Policies enforce `auth.uid() = user_id` for individual records.

#### Q98: Can a farmer see predictions created by another farmer?
**Ans:** No. Supabase RLS automatically filters query results at the database engine level based on the requester's authenticated UID.

#### Q99: Why is the Supabase `service_role` key never placed in Flutter?
**Ans:** Because Flutter client code can be decompiled; exposing the service-role key would bypass all RLS policies and compromise database security.

#### Q100: How is the Flutter UI designed for accessibility and farmer use?
**Ans:** Clean agricultural visual hierarchy, large legible typography, high-contrast color status indicators (green/orange/red), clear metric cards, and intuitive navigation.

#### Q101: How does the Flutter app connect to the backend during local development?
**Ans:** Uses `http://10.0.2.2:8000` for Android emulators (which bridges to host localhost), with a toggle in Settings for `http://127.0.0.1:8000` or custom cloud URLs.

#### Q102: How is the backend deployed?
**Ans:** Containerized via Docker (`Dockerfile`) and configured for cloud deployment via `render.yaml` running Uvicorn.

#### Q103: How is the Android APK built?
**Ans:** Via `flutter build apk --release` or the automated `build_apk.bat` script.

#### Q104: What automated test suites were written?
**Ans:** 10 Pytest backend integration tests (100% pass) and 5 Flutter unit/widget tests (100% pass).

#### Q105: What are the primary future improvements planned for CropGuard AI?
**Ans:** Integration of satellite multispectral NDVI imaging, IoT soil moisture probe telemetry, and local audio speech-to-text for vernacular voice queries.
