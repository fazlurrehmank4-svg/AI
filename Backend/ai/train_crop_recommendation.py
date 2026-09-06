"""
Crop Recommendation Model Training Pipeline
Trains an ensemble ML model (RandomForestClassifier + GradientBoosting)
on Data/Train/archive/Crop_recommendation.csv.
Features: N, P, K, temperature, humidity, ph, rainfall
Target: Crop label (22 categories)
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, f1_score

def train_crop_recommender(
    data_path: str = "Data/Train/archive/Crop_recommendation.csv",
    save_path: str = "Backend/ai/saved_models/crop_recommender.joblib"
):
    print("=" * 65)
    print("      TRAINING CROP RECOMMENDATION ENSEMBLE MODEL")
    print("=" * 65)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    df = pd.read_csv(data_path)
    print(f"[Data] Loaded {len(df)} samples from {data_path}")
    print(f"[Data] Target classes ({df['label'].nunique()}): {sorted(df['label'].unique().tolist())}")

    # Standardize column names
    df.columns = [c.strip().lower() for c in df.columns]
    feature_cols = ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[feature_cols].copy()
    y = df['label'].copy()

    # Label encoding
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Random Forest Classifier
    rf = RandomForestClassifier(
        n_estimators=150,
        max_depth=16,
        min_samples_split=2,
        random_state=42,
        n_jobs=-1
    )

    # Train Gradient Boosting Classifier
    gb = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    # Soft Voting Ensemble
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('gb', gb)],
        voting='soft'
    )

    print("[Training] Fitting Soft-Voting Ensemble (Random Forest + Gradient Boosting)...")
    ensemble.fit(X_train_scaled, y_train)

    # Evaluate on test set
    y_pred = ensemble.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')

    # Cross validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(ensemble, scaler.transform(X), y_encoded, cv=cv, scoring='accuracy')

    print(f"\n[Evaluation Results]")
    print(f"  - Test Accuracy:     {acc * 100:.2f}%")
    print(f"  - Test Macro F1:     {f1_macro:.4f}")
    print(f"  - 5-Fold CV Mean:    {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 100:.2f}%)")

    # Save artifact
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    artifact = {
        "model": ensemble,
        "scaler": scaler,
        "label_encoder": le,
        "feature_cols": feature_cols,
        "classes": le.classes_.tolist(),
        "metrics": {
            "test_accuracy": float(acc),
            "macro_f1": float(f1_macro),
            "cv_accuracy_mean": float(cv_scores.mean()),
            "cv_accuracy_std": float(cv_scores.std()),
            "sample_count": len(df)
        }
    }

    joblib.dump(artifact, save_path)
    print(f"[Artifact] Successfully saved model to {save_path}")

    return artifact

if __name__ == "__main__":
    train_crop_recommender()
