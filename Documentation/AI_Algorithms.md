# CropGuard AI: Mathematical Formulations & AI Algorithm Specifications

This document details the theoretical, mathematical, and algorithmic foundations of all 10 Artificial Intelligence components implemented in the CropGuard AI project.

---

## Practical 01: Data Engineering & Statistical Metrics
- **Mean:** $\bar{x} = \frac{1}{N}\sum_{i=1}^N x_i$
- **Standard Deviation:** $\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^N (x_i - \bar{x})^2}$
- **Z-Score Normalization:** $z_i = \frac{x_i - \mu}{\sigma}$

---

## Practical 02: Uninformed Search (BFS & DFS)
1. **Breadth-First Search (BFS):**
   - Implemented via a FIFO Queue.
   - Frontier: $Q \leftarrow \text{enqueue}(\text{start})$
   - Time Complexity: $\mathcal{O}(V + E)$
   - Guarantees the shortest path in unweighted risk graphs.
2. **Depth-First Search (DFS):**
   - Implemented via an explicit LIFO Stack.
   - Frontier: $S \leftarrow \text{push}(\text{start})$
   - Explores deep failure branches (worst-case pathological degradation).

---

## Practical 03: Informed Heuristic Search (GBFS & A*)
1. **Greedy Best-First Search (GBFS):**
   $$f(n) = h(n)$$
   Expands the node with the lowest heuristic distance to the goal. Rapid but can yield sub-optimal intervention paths.
2. **A\* Search:**
   $$f(n) = g(n) + h(n)$$
   Where:
   - $g(n)$: Exact accumulated cost from the start state to node $n$.
   - $h(n)$: Estimated heuristic cost from $n$ to the goal.
   - **Admissibility Condition:** $h(n) \le h^*(n)$ (never overestimates the true remaining cost).
   - **Consistency (Monotonicity):** $h(n) \le c(n, a, n') + h(n')$.
   - Guarantees finding the mathematically optimal, minimum-cost sequence of agronomic remediation actions.

---

## Practical 04: Local Search Optimization (Hill Climbing)
- **State Representation:** Coordinate tuple $s = (\text{irrigation\_mm}, \text{shade\_percent}) \in \mathbb{R}^2$.
- **Neighborhood Function:** 8-directional discrete step generator $N(s) = \{s + (\Delta i, \Delta s) \mid \Delta i, \Delta s \in \{-2, 0, 2\}\}$.
- **Objective Function:** Physiological Comfort Score $J(s) \in [0, 100]$, exhibiting multimodal peaks (local vs. global optimum).
- **Steepest Ascent Rule:**
  $$s_{t+1} = \arg\max_{s' \in N(s_t)} J(s')$$
  Terminates when $\max_{s' \in N(s_t)} J(s') \le J(s_t)$.
- **Random-Restart Hill Climbing:** Overcomes local maxima by executing independent trials from uniformly sampled random coordinates: $s_0 \sim \mathcal{U}(S)$.

---

## Practical 05: Propositional & First-Order Inference Engine
- **Inference Rule (Modus Ponens):**
  $$\frac{\alpha, \quad \alpha \implies \beta}{\beta}$$
- **Forward Chaining (Data-Driven):**
  Starts with observed fact set $F_0 = \{\text{fact}_1, \dots, \text{fact}_k\}$. Recursively evaluates:
  $$\text{If } \text{Premise}(R_i) \subseteq F_t \implies F_{t+1} = F_t \cup \{\text{Consequence}(R_i)\}$$
  Reaches fixpoint when $F_{t+1} = F_t$. Outputs deduced root causes and actionable precautions.
- **Backward Chaining (Goal-Driven Explainability):**
  Accepts hypothesis $G$. Finds rules $R$ concluding $G$. Recursively verifies if antecedents of $R$ are true in the knowledge base. Generates formal human-readable proof trees explaining why an alert was triggered.

---

## Practical 06: Multiple Linear Regression
- **Hypothesis Function:**
  $$\hat{y} = \beta_0 + \beta_1 X_{\text{temp}} + \beta_2 X_{\text{hum}} + \beta_3 X_{\text{rain}} + \beta_4 X_{\text{wind}}$$
- **Optimization Criterion (OLS Residual Sum of Squares):**
  $$J(\beta) = \sum_{i=1}^n (y_i - \hat{y}_i)^2$$
- **Closed-Form Solution:**
  $$\beta = (X^T X)^{-1} X^T y$$
- **Evaluation Metrics:**
  - **Mean Absolute Error (MAE):** $\frac{1}{n}\sum |y_i - \hat{y}_i|$
  - **Mean Squared Error (MSE):** $\frac{1}{n}\sum (y_i - \hat{y}_i)^2$
  - **Root Mean Squared Error (RMSE):** $\sqrt{\text{MSE}}$
  - **Coefficient of Determination ($R^2$):** $1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$

---

## Practical 07: Supervised Multiclass Classification
1. **k-Nearest Neighbors (k-NN):**
   - Metric: Euclidean Distance in $\mathbb{R}^d$:
     $$d(\mathbf{x}, \mathbf{x}') = \sqrt{\sum_{j=1}^d (x_j - x'_j)^2}$$
   - Decision Rule: Majority voting among the $k=5$ closest training exemplars.
2. **Decision Tree (CART):**
   - Splitting Criterion: Gini Impurity:
     $$I_G(p) = 1 - \sum_{i=1}^C p_i^2$$
   - Information Gain on split $S$:
     $$\Delta I_G = I_G(D) - \left(\frac{|D_L|}{|D|}I_G(D_L) + \frac{|D_R|}{|D|}I_G(D_R)\right)$$
   - Trees partition parameter space into orthogonal decision boundaries corresponding to `Healthy`, `At Risk`, and `High Risk`.

---

## Practical 08: Unsupervised K-Means Clustering
- **Objective Function (Inertia):**
  $$\mathcal{J} = \sum_{j=1}^k \sum_{\mathbf{x} \in S_j} \|\mathbf{x} - \boldsymbol{\mu}_j\|^2$$
- **k-Means++ Seeding:** Initializes first centroid uniformly, and subsequent centroids with probability proportional to squared distance:
  $$P(\mathbf{x}) = \frac{D(\mathbf{x})^2}{\sum_{\mathbf{x}'} D(\mathbf{x}')^2}$$
- **Silhouette Coefficient:**
  $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$
  Where $a(i)$ is mean intra-cluster distance and $b(i)$ is lowest mean distance to any other cluster.

---

## Practical 09: Domain-Specific NLP Knowledge Retrieval
- **Term Frequency (TF):**
  $$\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t' \in d} f_{t', d}}$$
- **Inverse Document Frequency (IDF):**
  $$\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + |\{d \in D \mid t \in d\}|}\right) + 1$$
- **TF-IDF Weighting:**
  $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$
- **Cosine Similarity Matching:**
  $$\text{Cosine Similarity}(\mathbf{q}, \mathbf{d}) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\| \|\mathbf{d}\|} = \frac{\sum q_i d_i}{\sqrt{\sum q_i^2} \sqrt{\sum d_i^2}}$$
- **Zero-Hallucination Thresholding:** If $\max_d \text{Cosine Similarity}(\mathbf{q}, \mathbf{d}) < 0.22$, the system rejects unsupported speculation and emits a transparent educational advisory.
