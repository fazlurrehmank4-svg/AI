# Practical 08: Agricultural Micro-Climate Regime Discovery via K-Means Clustering

---

## 1. What Is It?
Practical 08 applies unsupervised **K-Means Clustering** to partition agricultural meteorological observations into three distinct latent agro-ecological risk regimes without relying on pre-existing ground-truth labels.

## 2. Why Is It Used?
Weather operates as a coupled multi-dimensional system. Rather than examining temperature or rainfall in isolation, clustering discovers underlying environmental prototypes:
- **Cluster 0:** Favorable Agronomic Conditions
- **Cluster 1:** Moderate Climate Stress (Thermal/Moisture Anomaly)
- **Cluster 2:** Critical Weather Vulnerability (Extreme compound risk)

## 3. How Does It Work?
1. Normalizes input features (temperature, humidity, precipitation, wind speed) to standard zero-mean unit-variance space.
2. Initializes centroids using the **k-means++** smart seeding scheme.
3. Alternates between Expectation (assignment of samples to nearest Euclidean centroid) and Maximization (recomputing cluster centroid coordinates).
4. Quantifies clustering validity using the **Silhouette Coefficient** (measuring cluster cohesion vs. separation) and **Inertia** (within-cluster sum of squares).
5. Visualizes 2D slices with centroids marked as prominent 'X' anchors (`kmeans_clusters_visualization.png`).

## 4. Inputs & Outputs
- **Input:** Meteorological parameters: Temperature (°C), Humidity (%), Rainfall (mm), Wind Speed (km/h).
- **Output:** Cluster ID assignment ($0, 1, 2$), cluster regime title, centroid coordinates, and visualization plot.

## 5. Time & Space Complexity
- **Time Complexity:** $\mathcal{O}(I \cdot K \cdot n \cdot d)$ where $I$ is iterations ($\approx 15$), $K=3$, $n=2,400$, and $d=4$. Fits in $< 0.1$ seconds.
- **Space Complexity:** $\mathcal{O}(n \cdot d + K \cdot d)$ for points and centroid representations.

## 6. Project Connection
Supplies CropGuard AI's **Agro-Climatic Zone Identifier**, grouping the farmer's current geographic microclimate into an intuitive regional macro-profile.

## 7. Limitations
Assumes spherical clusters of similar variance and requires specifying cluster count $k$ a priori.

## 8. Runnable Command
```bash
python Practical_08_Clustering/clustering_model.py
```
