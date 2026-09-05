"""
Practical 08: Agricultural Micro-Climate Regime Discovery via K-Means Clustering
Author: CropGuard AI Team
Description:
    Applies Unsupervised K-Means Clustering to discover latent environmental
    vulnerability regimes across agricultural weather observations without label supervision.
    Identifies 3 primary clusters:
      Cluster 0: Favorable Agronomic Conditions
      Cluster 1: Moderate Climate Stress (Thermal / Moisture Anomaly)
      Cluster 2: Critical Extreme Weather Vulnerability
    Evaluates Silhouette Score, Inertia (Elbow method), and visualizes 2D clusters with Centroids.
"""

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

def train_and_evaluate_clustering(
    data_path="Data/processed/crop_weather_data.csv",
    output_dir="Practical_08_Clustering",
    save_model_path=None
):
    os.makedirs(output_dir, exist_ok=True)
    print("=" * 60)
    print("PRACTICAL 08: K-MEANS CLUSTERING OF AGRICULTURAL ENVIRONMENTS")
    print("=" * 60)

    # 1. Ingest Data
    df = pd.read_csv(data_path)
    feature_cols = ["temperature", "humidity", "rainfall", "wind_speed"]
    X = df[feature_cols]

    # 2. Scale Features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. K-Means Clustering (k=3)
    k = 3
    kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    df["cluster"] = clusters

    # 4. Evaluation Metrics
    sil_score = silhouette_score(X_scaled, clusters)
    inertia = kmeans.inertia_

    print("\n--- Clustering Diagnostics ---")
    print(f"Optimal Clusters (k):     {k}")
    print(f"Inertia (Within-SS):      {inertia:.2f}")
    print(f"Silhouette Coefficient:   {sil_score:.4f}")

    # Analyze Cluster Centroid Profiles (In original unscaled feature units)
    centroids_unscaled = scaler.inverse_transform(kmeans.cluster_centers_)
    centroid_df = pd.DataFrame(centroids_unscaled, columns=feature_cols)

    # Calculate average health score per cluster for semantic naming
    cluster_health = df.groupby("cluster")["crop_health_score"].mean()

    # Assign agronomic labels based on health scores
    sorted_cluster_indices = cluster_health.sort_values(ascending=False).index.tolist()
    label_map = {
        sorted_cluster_indices[0]: "Favorable Agronomic Regime",
        sorted_cluster_indices[1]: "Moderate Climate Stress",
        sorted_cluster_indices[2]: "Critical Weather Vulnerability"
    }

    print("\n--- Unscaled Cluster Centroids & Agronomic Characterization ---")
    for c_id in range(k):
        label = label_map[c_id]
        mean_health = cluster_health[c_id]
        c_row = centroid_df.iloc[c_id]
        print(f"\nCluster {c_id}: [{label}] (Mean Health Score: {mean_health:.1f}/100)")
        print(f"  Temp: {c_row['temperature']:.1f}°C | Humidity: {c_row['humidity']:.1f}% | Rain: {c_row['rainfall']:.1f}mm | Wind: {c_row['wind_speed']:.1f}km/h")

    # 5. Visualizations
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Practical 08: K-Means Clustering of Agricultural Micro-Climates", fontsize=14, fontweight='bold', color='#1B5E20')

    colors = ['#2E7D32', '#FB8C00', '#D32F2F']
    # Plot 1: Temperature vs Humidity
    for c_id in range(k):
        sub = df[df["cluster"] == c_id]
        axes[0].scatter(
            sub["temperature"], sub["humidity"],
            label=f"Cluster {c_id}: {label_map[c_id]}",
            color=colors[c_id], alpha=0.5, s=25, edgecolors='none'
        )
    # Plot Centroids
    axes[0].scatter(
        centroids_unscaled[:, 0], centroids_unscaled[:, 1],
        color='black', marker='X', s=160, linewidths=2, label='Cluster Centroids'
    )
    axes[0].set_title("Temperature vs. Relative Humidity", fontweight='bold')
    axes[0].set_xlabel("Temperature (°C)")
    axes[0].set_ylabel("Humidity (%)")
    axes[0].legend(fontsize=8, loc='upper left')
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # Plot 2: Humidity vs Rainfall
    for c_id in range(k):
        sub = df[df["cluster"] == c_id]
        axes[1].scatter(
            sub["humidity"], sub["rainfall"],
            label=f"Cluster {c_id}: {label_map[c_id]}",
            color=colors[c_id], alpha=0.5, s=25, edgecolors='none'
        )
    axes[1].scatter(
        centroids_unscaled[:, 1], centroids_unscaled[:, 2],
        color='black', marker='X', s=160, linewidths=2, label='Cluster Centroids'
    )
    axes[1].set_title("Humidity vs. Rainfall", fontweight='bold')
    axes[1].set_xlabel("Humidity (%)")
    axes[1].set_ylabel("Rainfall (mm)")
    axes[1].legend(fontsize=8, loc='upper left')
    axes[1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plot_path = os.path.join(output_dir, "kmeans_clusters_visualization.png")
    plt.savefig(plot_path, dpi=200)
    plt.close()
    print(f"\n[+] Clustering visual graphic saved to: {plot_path}")

    # 6. Save serialized artifacts if requested
    if save_model_path:
        os.makedirs(os.path.dirname(save_model_path), exist_ok=True)
        joblib.dump({
            "model": kmeans,
            "scaler": scaler,
            "feature_cols": feature_cols,
            "centroids_unscaled": centroids_unscaled,
            "label_map": label_map
        }, save_model_path)
        print(f"[+] Serialized K-Means artifact saved to: {save_model_path}")

    return {
        "silhouette_score": round(sil_score, 4),
        "inertia": round(inertia, 2),
        "label_map": label_map
    }

if __name__ == "__main__":
    train_and_evaluate_clustering(save_model_path="Backend/ai/saved_models/kmeans_model.joblib")
