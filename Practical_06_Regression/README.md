# Practical 06: Continuous Crop Health Prediction via Linear Regression

---

## 1. What Is It?
Practical 06 implements multiple **Linear Regression** to predict an unconstrained continuous agronomic index—the **Crop Health Score** ($0.0 \le y \le 100.0$)—using four primary meteorological regressors: temperature, relative humidity, rainfall, and wind speed.

## 2. Why Is It Used?
Discrete categories (`Healthy` vs `Unhealthy`) lack fine granularity. A farmer needs to observe gradual physiological stress (e.g. drop from 95 to 78 score) before macroscopic necrosis or irreversible wilting occurs. Linear regression provides continuous gradient tracking.

## 3. How Does It Work?
1. Evaluates Ordinary Least Squares (OLS) optimization:
   $$\hat{y} = \beta_0 + \beta_1 X_{\text{temp}} + \beta_2 X_{\text{hum}} + \beta_3 X_{\text{rain}} + \beta_4 X_{\text{wind}}$$
2. Standardizes meteorological features using z-score normalization (`StandardScaler`).
3. Evaluates error residuals across test splits using standard regression metrics:
   - **Mean Absolute Error (MAE)**: $\frac{1}{n} \sum |y - \hat{y}|$
   - **Mean Squared Error (MSE)**: $\frac{1}{n} \sum (y - \hat{y})^2$
   - **Root Mean Squared Error (RMSE)**: $\sqrt{\text{MSE}}$
   - **$R^2$ Score**: Proportion of variance explained by the model.
4. Generates an evaluation graphic (`regression_evaluation.png`).

## 4. Inputs & Outputs
- **Input:** 4 continuous weather features: Temperature (°C), Humidity (%), Rainfall (mm), Wind Speed (km/h).
- **Output:** Continuous predicted health score ($0-100$), regression weights ($\beta$), residual metrics, and serialized model artifact.

## 5. Time & Space Complexity
- **Training Time:** $\mathcal{O}(d^2 n + d^3)$ where $n$ is sample size (1,920 train) and $d$ is feature count (4). Fits in $< 0.05$ seconds.
- **Inference Time:** $\mathcal{O}(d)$, executing in $< 0.1$ milliseconds per prediction.

## 6. Project Connection
Supplies the continuous numerical score gauge rendered on the CropGuard AI Home Dashboard and Prediction Screen, calibrated alongside the classification predictions.

## 7. Limitations
Linear regression presumes linear monotonic relationships; non-linear thresholds (e.g., fungal outbreaks triggered abruptly when humidity exceeds 85%) require complementary non-linear classifiers and rule engines.

## 8. Runnable Command
```bash
python Practical_06_Regression/regression_model.py
```
