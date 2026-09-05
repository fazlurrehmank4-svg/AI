# Practical 01: Python Environment, Data Preprocessing & Visualization

---

## 1. What Is It?
Practical 01 establishes the foundational data engineering and exploratory data analysis (EDA) pipeline using Python, NumPy, Pandas, and Matplotlib to analyze Kaggle-derived weather and crop health data.

## 2. Why Is It Used?
Before training machine learning models or deploying reasoning engines, agricultural datasets must be audited for missing values, outliers, distributional skew, and correlation between meteorological drivers (temperature, humidity, precipitation, wind speed) and crop vigor.

## 3. How Does It Work?
1. Ingests raw and processed CSV datasets via Pandas.
2. Generates parametric statistical profiles (mean, standard deviation, quartiles).
3. Performs integrity checks (verifying 0 missing records).
4. Computes cross-crop summaries (temperatures, humidities, and average health indices).
5. Renders a publication-ready 4-panel visual graphic (`weather_crop_analysis.png`) depicting:
   - Health score histogram.
   - Temperature vs. Health score scatter plot.
   - Categorical health status class counts (`Healthy`, `At Risk`, `High Risk`).
   - Multivariate humidity vs. rainfall scatter with colormap encoding health scores.

## 4. Inputs & Outputs
- **Input:** `Data/processed/crop_weather_data.csv` (2,400 observations across 8 crops).
- **Output:** Descriptive statistics printed to standard output and `weather_crop_analysis.png`.

## 5. Time & Space Complexity
- **Time Complexity:** $\mathcal{O}(N \times M)$ where $N$ is the number of samples (2,400) and $M$ is the number of features. Execution takes $< 1.5$ seconds.
- **Space Complexity:** $\mathcal{O}(N \times M)$ memory allocation for the Pandas DataFrame and Matplotlib figure canvas.

## 6. Project Connection
Practical 01 prepares the clean datasets ingested by:
- Practical 06 (Linear Regression)
- Practical 07 (k-NN & Decision Tree Classification)
- Practical 08 (K-Means Clustering)
- Backend inference engines (`Backend/ai/`)

## 7. Limitations
Descriptive statistics and static plots uncover global correlations but do not perform non-linear boundary separation or causal inference; predictive modeling requires the subsequent machine learning practicals.

## 8. Runnable Command
```bash
python Practical_01_Python_Environment/main.py
```
