"""
Practical 06: Continuous Crop Health Score Prediction via Linear Regression
Author: CropGuard AI Team
Description:
    Trains a Linear Regression model on meteorological variables
    (temperature, humidity, rainfall, wind_speed) to predict continuous
    Crop Health Score (0-100).
    Evaluates Mean Absolute Error (MAE), Mean Squared Error (MSE),
    Root Mean Squared Error (RMSE), and Coefficient of Determination (R^2).
"""

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

def train_and_evaluate_regression(
    data_path="Data/processed/crop_weather_data.csv",
    output_dir="Practical_06_Regression",
    save_model_path=None
):
    os.makedirs(output_dir, exist_ok=True)
    print("=" * 60)
    print("PRACTICAL 06: LINEAR REGRESSION CROP HEALTH PREDICTION")
    print("=" * 60)

    # 1. Load Data
    df = pd.read_csv(data_path)
    feature_cols = ["temperature", "humidity", "rainfall", "wind_speed"]
    target_col = "crop_health_score"

    X = df[feature_cols]
    y = df[target_col]

    # 2. Train-Test Split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    # 3. Fit Standard Scaler & Model
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # 4. Predictions & Evaluation
    y_pred = model.predict(X_test_scaled)
    # Clip predictions to logical physical bounds [0, 100]
    y_pred = np.clip(y_pred, 0.0, 100.0)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("\n--- Model Evaluation Metrics ---")
    print(f"Mean Absolute Error (MAE):     {mae:.2f}")
    print(f"Mean Squared Error (MSE):      {mse:.2f}")
    print(f"Root Mean Squared Error (RMSE):{rmse:.2f}")
    print(f"R-squared Score (R^2):         {r2:.4f}")

    print("\n--- Regression Feature Coefficients ---")
    for feat, coef in zip(feature_cols, model.coef_):
        print(f"  {feat:<15}: {coef:+.3f}")
    print(f"  {'Intercept':<15}: {model.intercept_:+.3f}")

    # 5. Visualizations
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Practical 06: Linear Regression - Crop Health Score Evaluation", fontsize=14, fontweight='bold', color='#1B5E20')

    # Actual vs Predicted Scatter
    axes[0].scatter(y_test, y_pred, color='#2E7D32', alpha=0.6, edgecolors='none', label='Test Samples')
    axes[0].plot([0, 100], [0, 100], color='#D32F2F', linestyle='--', linewidth=2, label='Ideal 1:1 Parity')
    axes[0].set_title(f"Actual vs. Predicted ($R^2 = {r2:.3f}$)", fontweight='bold')
    axes[0].set_xlabel("Actual Health Score")
    axes[0].set_ylabel("Predicted Health Score")
    axes[0].legend()
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # Residuals Distribution
    residuals = y_test - y_pred
    axes[1].hist(residuals, bins=25, color='#43A047', edgecolor='#1B5E20', alpha=0.8)
    axes[1].axvline(0, color='red', linestyle='--', linewidth=1.5)
    axes[1].set_title(f"Residuals Distribution (RMSE = {rmse:.2f})", fontweight='bold')
    axes[1].set_xlabel("Prediction Error (Residual)")
    axes[1].set_ylabel("Frequency")
    axes[1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plot_path = os.path.join(output_dir, "regression_evaluation.png")
    plt.savefig(plot_path, dpi=200)
    plt.close()
    print(f"\n[+] Regression evaluation plot saved to: {plot_path}")

    # 6. Save serialized artifacts if requested
    if save_model_path:
        os.makedirs(os.path.dirname(save_model_path), exist_ok=True)
        artifact = {
            "model": model,
            "scaler": scaler,
            "feature_cols": feature_cols,
            "metrics": {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}
        }
        joblib.dump(artifact, save_model_path)
        print(f"[+] Serialized model artifact saved to: {save_model_path}")

    return {
        "mae": round(mae, 2),
        "mse": round(mse, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 4)
    }

if __name__ == "__main__":
    train_and_evaluate_regression(save_model_path="Backend/ai/saved_models/linear_regression.joblib")
