"""
Practical 01: Python Environment, NumPy, Pandas, Matplotlib for Agricultural Data Analysis
Author: CropGuard AI Team
Description:
    Demonstrates data ingestion, cleaning, statistical profiling, and
    multivariate correlation visualization between weather variables and
    crop health indicators using Kaggle agricultural datasets.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_practical_01(data_path="Data/processed/crop_weather_data.csv", output_dir="Practical_01_Python_Environment"):
    os.makedirs(output_dir, exist_ok=True)
    print("=" * 60)
    print("PRACTICAL 01: AGRICULTURAL DATA PREPROCESSING & EDA")
    print("=" * 60)

    # 1. Load dataset
    df = pd.read_csv(data_path)
    print(f"[+] Loaded dataset successfully from: {data_path}")
    print(f"[+] Total Records: {df.shape[0]} | Features: {df.shape[1]}")

    # 2. Statistical Summary
    print("\n--- Summary Statistics (Weather & Health) ---")
    numeric_cols = ["temperature", "humidity", "rainfall", "wind_speed", "crop_health_score"]
    stats_df = df[numeric_cols].describe()
    print(stats_df.round(2))

    # 3. Missing Value & Integrity Audit
    missing = df.isnull().sum()
    print("\n--- Data Integrity Audit (Missing Values) ---")
    print(missing[missing > 0] if missing.sum() > 0 else "Zero missing values detected. Clean data.")

    # 4. Crop Grouping Analysis
    print("\n--- Mean Health Score & Primary Risk per Crop ---")
    crop_stats = df.groupby("crop").agg({
        "crop_health_score": ["mean", "min", "max"],
        "temperature": "mean",
        "humidity": "mean",
        "rainfall": "mean"
    }).round(2)
    print(crop_stats)

    # 5. Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Practical 01: CropGuard AI - Weather & Crop Health Analysis", fontsize=16, fontweight='bold', color='#1B5E20')

    # Plot 1: Health Score Distribution
    axes[0, 0].hist(df["crop_health_score"], bins=20, color='#4CAF50', edgecolor='#1B5E20', alpha=0.85)
    axes[0, 0].set_title("Distribution of Crop Health Scores (0-100)", fontweight='bold')
    axes[0, 0].set_xlabel("Health Score")
    axes[0, 0].set_ylabel("Frequency")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)

    # Plot 2: Temperature vs Crop Health Score Scatter
    crops_sample = df["crop"].unique()[:4]
    palette = ['#E53935', '#1E88E5', '#43A047', '#FB8C00']
    for idx, crop in enumerate(crops_sample):
        sub = df[df["crop"] == crop]
        axes[0, 1].scatter(sub["temperature"], sub["crop_health_score"], label=crop, color=palette[idx], alpha=0.6, edgecolors='none')
    axes[0, 1].set_title("Temperature vs Crop Health Score", fontweight='bold')
    axes[0, 1].set_xlabel("Temperature (°C)")
    axes[0, 1].set_ylabel("Crop Health Score")
    axes[0, 1].legend()
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)

    # Plot 3: Health Status Bar Chart
    status_counts = df["health_status"].value_counts()
    colors = ['#4CAF50', '#FFA000', '#D32F2F']
    axes[1, 0].bar(status_counts.index, status_counts.values, color=colors, edgecolor='#333333')
    axes[1, 0].set_title("Health Status Classification Frequency", fontweight='bold')
    axes[1, 0].set_ylabel("Count")
    for i, v in enumerate(status_counts.values):
        axes[1, 0].text(i, v + 25, str(v), ha='center', fontweight='bold')
    axes[1, 0].grid(True, linestyle="--", alpha=0.5, axis='y')

    # Plot 4: Humidity vs Rainfall Risk Bubble Chart
    scatter = axes[1, 1].scatter(
        df["humidity"], df["rainfall"],
        c=df["crop_health_score"], cmap="RdYlGn",
        alpha=0.65, edgecolors='gray', linewidth=0.5
    )
    axes[1, 1].set_title("Humidity vs Rainfall (Color = Health Score)", fontweight='bold')
    axes[1, 1].set_xlabel("Relative Humidity (%)")
    axes[1, 1].set_ylabel("Rainfall (mm)")
    cbar = fig.colorbar(scatter, ax=axes[1, 1])
    cbar.set_label("Crop Health Score")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plot_path = os.path.join(output_dir, "weather_crop_analysis.png")
    plt.savefig(plot_path, dpi=200)
    plt.close()
    print(f"\n[+] Statistical plots successfully rendered and saved to: {plot_path}")
    return stats_df

if __name__ == "__main__":
    run_practical_01()
