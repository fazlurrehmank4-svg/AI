# Practical 07: Multiclass Crop Health Classification (k-NN & Decision Tree)

---

## 1. What Is It?
Practical 07 implements and compares two canonical supervised machine learning classifiers—**k-Nearest Neighbors (k-NN)** and **Decision Tree Classifier**—to categorize agricultural health states into three operational risk tiers:
1. `Healthy` (Vigorous growth within optimal envelope)
2. `At Risk` (Moderate abiotic/weather stress)
3. `High Risk` (Extreme pathology risk or physiological failure)

## 2. Why Is It Used?
Field decisions demand categorical prioritization. Agricultural extension agents need actionable categorization rather than floating-point values alone. Furthermore, comparing an instance-based classifier (k-NN) with a symbolic rule-based tree (Decision Tree) allows benchmarking generalization accuracy versus computational latency.

## 3. How Does It Work?
- **k-NN ($k=5$):** Calculates Euclidean distance in normalized metric space $\mathbb{R}^5$ (temperature, humidity, rainfall, wind speed, soil pH). Assigns class by majority vote among nearest neighbors.
- **Decision Tree (CART, max depth = 6):** Recursively minimizes Gini impurity:
  $$G = 1 - \sum_{i=1}^C p_i^2$$
  to construct explainable orthogonal decision thresholds.
- **Metrics Evaluated:** Overall Accuracy, Precision, Recall, Macro F1-score, and side-by-side Confusion Matrices.

## 4. Inputs & Outputs
- **Input:** Meteorological and edaphic features: Temperature (°C), Humidity (%), Rainfall (mm), Wind Speed (km/h), Soil pH.
- **Output:** Categorical label (`Healthy`, `At Risk`, `High Risk`), class probability distribution, and confusion matrix graphic (`classification_confusion_matrices.png`).

## 5. Time & Space Complexity
- **k-NN:** Training time $\mathcal{O}(1)$; inference time $\mathcal{O}(n \cdot d)$.
- **Decision Tree:** Training time $\mathcal{O}(n \cdot d \log n)$; inference time $\mathcal{O}(\text{depth})$, running in $< 0.05$ milliseconds.

## 6. Project Connection
Supplies the primary categorical risk status displayed in the CropGuard AI header badge, color-coded as Green (`Healthy`), Orange (`At Risk`), or Red (`High Risk`).

## 7. Limitations
k-NN requires storing all training exemplars and is sensitive to irrelevant features; Decision Trees can suffer from axis-aligned variance, which we mitigate by constraining maximum tree depth.

## 8. Runnable Command
```bash
python Practical_07_Classification/classification_models.py
```
