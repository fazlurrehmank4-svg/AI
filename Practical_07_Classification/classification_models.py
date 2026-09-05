"""
Practical 07: Multiclass Crop Health Classification via k-NN & Decision Tree
Author: CropGuard AI Team
Description:
    Trains and benchmarks two fundamental machine learning classifiers:
    1. k-Nearest Neighbors (k-NN) - Instance-based non-parametric classifier.
    2. Decision Tree Classifier - Rule-based recursive partitioning tree.
    Predicts categorical crop condition: ['Healthy', 'At Risk', 'High Risk'].
    Evaluates Accuracy, Precision, Recall, Macro F1-score, and Confusion Matrices.
"""

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

def train_and_evaluate_classifiers(
    data_path="Data/processed/crop_weather_data.csv",
    output_dir="Practical_07_Classification",
    save_model_dir=None
):
    os.makedirs(output_dir, exist_ok=True)
    print("=" * 60)
    print("PRACTICAL 07: CROP HEALTH CLASSIFICATION (k-NN & DECISION TREE)")
    print("=" * 60)

    # 1. Ingest Data
    df = pd.read_csv(data_path)
    feature_cols = ["temperature", "humidity", "rainfall", "wind_speed", "soil_ph"]
    target_col = "health_status"

    X = df[feature_cols]
    y_raw = df[target_col]

    # Label encoding target classes
    label_encoder = LabelEncoder()
    # Ensure specific order: Healthy, At Risk, High Risk
    classes_order = ["Healthy", "At Risk", "High Risk"]
    label_encoder.fit(classes_order)
    y = label_encoder.transform(y_raw)

    # 2. Train-Test Split (80/20 stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 3. Model 1: k-Nearest Neighbors
    knn = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
    knn.fit(X_train_scaled, y_train)
    y_pred_knn = knn.predict(X_test_scaled)
    acc_knn = accuracy_score(y_test, y_pred_knn)
    f1_knn = f1_score(y_test, y_pred_knn, average='macro')

    # 4. Model 2: Decision Tree Classifier
    dt = DecisionTreeClassifier(max_depth=6, criterion='gini', random_state=42)
    dt.fit(X_train, y_train)  # Decision trees do not require feature scaling
    y_pred_dt = dt.predict(X_test)
    acc_dt = accuracy_score(y_test, y_pred_dt)
    f1_dt = f1_score(y_test, y_pred_dt, average='macro')

    print("\n" + "-" * 50)
    print("Model 1: k-Nearest Neighbors (k=5)")
    print("-" * 50)
    print(f"Overall Accuracy:  {acc_knn * 100:.2f}%")
    print(f"Macro F1-Score:    {f1_knn:.4f}")
    print("\nk-NN Detailed Classification Report:")
    print(classification_report(y_test, y_pred_knn, target_names=classes_order))

    print("-" * 50)
    print("Model 2: Decision Tree Classifier (max_depth=6)")
    print("-" * 50)
    print(f"Overall Accuracy:  {acc_dt * 100:.2f}%")
    print(f"Macro F1-Score:    {f1_dt:.4f}")
    print("\nDecision Tree Detailed Classification Report:")
    print(classification_report(y_test, y_pred_dt, target_names=classes_order))

    # 5. Visualizations: Confusion Matrices
    cm_knn = confusion_matrix(y_test, y_pred_knn)
    cm_dt = confusion_matrix(y_test, y_pred_dt)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Practical 07: Confusion Matrix Comparison (k-NN vs Decision Tree)", fontsize=14, fontweight='bold', color='#1B5E20')

    for ax, cm, title, acc in zip(
        axes,
        [cm_knn, cm_dt],
        ["k-NN (k=5)", "Decision Tree (depth=6)"],
        [acc_knn, acc_dt]
    ):
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
        ax.set_title(f"{title}\nAccuracy: {acc*100:.1f}%", fontweight='bold')
        tick_marks = np.arange(len(classes_order))
        ax.set_xticks(tick_marks)
        ax.set_xticklabels(classes_order)
        ax.set_yticks(tick_marks)
        ax.set_yticklabels(classes_order)
        ax.set_xlabel("Predicted Label")
        ax.set_ylabel("True Label")

        # Overlay counts inside cells
        thresh = cm.max() / 2.0
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], 'd'),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black",
                        fontweight='bold')

    plt.tight_layout()
    plot_path = os.path.join(output_dir, "classification_confusion_matrices.png")
    plt.savefig(plot_path, dpi=200)
    plt.close()
    print(f"\n[+] Confusion matrix graphic saved to: {plot_path}")

    # 6. Save serialized artifacts if requested
    if save_model_dir:
        os.makedirs(save_model_dir, exist_ok=True)
        joblib.dump({
            "model": knn,
            "scaler": scaler,
            "classes": classes_order,
            "feature_cols": feature_cols
        }, os.path.join(save_model_dir, "knn_model.joblib"))

        joblib.dump({
            "model": dt,
            "classes": classes_order,
            "feature_cols": feature_cols
        }, os.path.join(save_model_dir, "decision_tree_model.joblib"))
        print(f"[+] Serialized classification models saved to: {save_model_dir}")

    return {
        "knn": {"accuracy": round(acc_knn, 4), "macro_f1": round(f1_knn, 4)},
        "dt": {"accuracy": round(acc_dt, 4), "macro_f1": round(f1_dt, 4)}
    }

if __name__ == "__main__":
    train_and_evaluate_classifiers(save_model_dir="Backend/ai/saved_models")
