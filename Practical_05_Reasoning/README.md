# Practical 05: Forward & Backward Chaining Reasoning Engine

---

## 1. What Is It?
Practical 05 implements a formal First-Order / Propositional Expert System inference engine featuring both **Forward Chaining (data-driven deduction)** and **Backward Chaining (goal-driven proof & explainability)** for agricultural disease etiology and precaution synthesis.

## 2. Why Is It Used?
Machine learning classifiers output probability vectors (e.g. `High Risk`), but farmers require transparent, legally responsible, and auditable causal explanations: *Why* is the risk high? *What* are the root environmental causes? *What* concrete precautions should be performed immediately?

## 3. How Does It Work?
- **Fact Extraction:** Discretizes numerical weather parameters into semantic facts (`humidity_high`, `rainfall_high`, `temperature_high`, `wind_strong`).
- **Forward Chaining:** Ingests the initial fact set and applies Modus Ponens repeatedly across domain rules. Deduces risk diagnoses, root causes, and actionable precaution checklists until reaching fixpoint.
- **Backward Chaining:** Accepts a target hypothesis (e.g. `fungal_disease_risk_high`) and traverses backward through rule premises to verify if current observations satisfy every required antecedent. Emits human-readable agronomic justification strings.

## 4. Inputs & Outputs
- **Input:** Meteorological sensor variables (temperature, relative humidity, precipitation, wind speed) and optional diagnostic goals.
- **Output:** Set of fired rules, deduplicated root causes, prioritized precautions, and backward-chaining justification proofs.

## 5. Time & Space Complexity
- **Time Complexity:** $\mathcal{O}(R \times C)$ where $R$ is the number of rules and $C$ is the average number of conditions per rule. Runs in $< 5$ milliseconds.
- **Space Complexity:** $\mathcal{O}(F + R)$ where $F$ is the working memory fact set.

## 6. Project Connection
Practical 05 directly powers the CropGuard AI **Causes and Precautions Screen** and provides the core reasoning substrate for the **Local NLP Farmer Chatbot** (Practical 09 & `Backend/ai/`).

## 7. Limitations
Requires curated domain knowledge rules; extreme novel scenarios outside the rule base must fall back to conservative advisories.

## 8. Runnable Command
```bash
python Practical_05_Reasoning/reasoning_engine.py
```
