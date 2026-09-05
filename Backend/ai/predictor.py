"""
CropGuard AI Unified Predictor Engine
Coordinates:
  - Regression Model (Continuous Health Score 0-100)
  - Classification Model (Healthy / At Risk / High Risk)
  - K-Means Clustering (Agro-Climatic Regime)
  - Forward Chaining Inference (Causes & Precautions)
  - Backward Chaining Verification (Explainability)
"""

import os
import json
import joblib
import numpy as np
from datetime import datetime
from typing import Dict, Any, List

import sys
sys.path.append(os.path.abspath("Practical_05_Reasoning"))
from reasoning_engine import AgriculturalReasoningEngine

class CropGuardPredictor:
    def __init__(
        self,
        models_dir: str = "Backend/ai/saved_models",
        knowledge_base_path: str = "Data/knowledge_base/crop_knowledge.json"
    ):
        self.models_dir = models_dir
        self.reasoning_engine = AgriculturalReasoningEngine()
        self.knowledge_base = {}

        if os.path.exists(knowledge_base_path):
            with open(knowledge_base_path, "r") as f:
                self.knowledge_base = json.load(f)

        # Load ML artifacts
        self.reg_artifact = self._load_joblib("linear_regression.joblib")
        self.dt_artifact = self._load_joblib("decision_tree_model.joblib")
        self.knn_artifact = self._load_joblib("knn_model.joblib")
        self.kmeans_artifact = self._load_joblib("kmeans_model.joblib")

    def _load_joblib(self, filename: str):
        path = os.path.join(self.models_dir, filename)
        if os.path.exists(path):
            try:
                return joblib.load(path)
            except Exception as e:
                print(f"[Predictor] Error loading {filename}: {e}")
        return None

    def predict(
        self,
        crop: str,
        temperature: float,
        humidity: float,
        rainfall: float,
        wind_speed: float,
        soil_ph: float = 6.5,
        location_name: str = "Field Station"
    ) -> Dict[str, Any]:
        """
        Executes end-to-end multi-model inference and reasoning.
        """
        crop_clean = crop.capitalize()

        # 1. Regression Inference (Crop Health Score)
        if self.reg_artifact and "model" in self.reg_artifact and "scaler" in self.reg_artifact:
            features_reg = np.array([[temperature, humidity, rainfall, wind_speed]])
            features_scaled = self.reg_artifact["scaler"].transform(features_reg)
            raw_score = float(self.reg_artifact["model"].predict(features_scaled)[0])
            health_score = round(float(np.clip(raw_score, 5.0, 98.0)), 1)
        else:
            health_score = 75.0  # Fallback baseline

        # 2. Classification Inference (Health Status)
        if self.dt_artifact and "model" in self.dt_artifact:
            # Features: [temperature, humidity, rainfall, wind_speed, soil_ph]
            features_dt = np.array([[temperature, humidity, rainfall, wind_speed, soil_ph]])
            class_idx = int(self.dt_artifact["model"].predict(features_dt)[0])
            classes = self.dt_artifact.get("classes", ["Healthy", "At Risk", "High Risk"])
            health_status = classes[class_idx]
        else:
            if health_score >= 75:
                health_status = "Healthy"
            elif health_score >= 50:
                health_status = "At Risk"
            else:
                health_status = "High Risk"

        # Map to Risk Level
        risk_map = {
            "Healthy": "Low",
            "At Risk": "Moderate",
            "High Risk": "High"
        }
        risk_level = risk_map.get(health_status, "Moderate")

        # 3. K-Means Clustering (Agro-Climatic Regime)
        regime_label = "Temperate Agricultural Zone"
        if self.kmeans_artifact and "model" in self.kmeans_artifact and "scaler" in self.kmeans_artifact:
            features_km = np.array([[temperature, humidity, rainfall, wind_speed]])
            features_km_scaled = self.kmeans_artifact["scaler"].transform(features_km)
            cluster_id = int(self.kmeans_artifact["model"].predict(features_km_scaled)[0])
            regime_label = self.kmeans_artifact.get("label_map", {}).get(cluster_id, f"Climatic Cluster {cluster_id}")

        # 4. Forward Chaining Reasoning (Causes & Precautions)
        facts = self.reasoning_engine.extract_facts_from_weather(temperature, humidity, rainfall, wind_speed)
        fc_res = self.reasoning_engine.forward_chaining(facts)

        causes = fc_res.get("causes", [])
        precautions = fc_res.get("precautions", [])

        # Enrich causes & precautions with crop-specific knowledge base
        if crop_clean in self.knowledge_base:
            kb_crop = self.knowledge_base[crop_clean]
            t_min, t_max = kb_crop["temp_optimal"]
            h_min, h_max = kb_crop["humidity_optimal"]
            r_min, r_max = kb_crop["rainfall_optimal"]

            if temperature < t_min:
                causes.insert(0, f"Ambient temperature ({temperature:.1f}°C) is below {crop_clean}'s optimal minimum of {t_min}°C.")
            elif temperature > t_max:
                causes.insert(0, f"Ambient temperature ({temperature:.1f}°C) exceeds {crop_clean}'s optimal threshold of {t_max}°C.")

            if humidity > h_max:
                causes.append(f"Relative humidity ({humidity:.1f}%) exceeds recommended ceiling of {h_max}%, elevating foliar fungal risk.")

            if rainfall > r_max:
                causes.append(f"Rainfall ({rainfall:.1f} mm) is higher than {crop_clean}'s optimal ceiling of {r_max} mm, creating waterlogging risk.")

            # Append general agronomic precautions if needed
            for p in kb_crop.get("precautions", []):
                if p not in precautions:
                    precautions.append(p)

        if not causes:
            causes = ["Meteorological parameters remain within acceptable biological envelopes for this crop."]
        if not precautions:
            precautions = ["Maintain scheduled scoutings and follow standard irrigation management."]

        # 5. Backward Chaining Explanation
        if "fungal_disease_risk_high" in fc_res["final_facts"]:
            _, _, explanation = self.reasoning_engine.backward_chaining("fungal_disease_risk_high", facts)
        elif "heat_and_drought_stress_severe" in fc_res["final_facts"]:
            _, _, explanation = self.reasoning_engine.backward_chaining("heat_and_drought_stress_severe", facts)
        elif health_status == "Healthy":
            explanation = f"Current weather conditions (Temp: {temperature}°C, Humidity: {humidity}%) align with optimal physiological thresholds for {crop_clean}."
        else:
            explanation = f"Health status '{health_status}' deduced because observed weather parameters deviate from {crop_clean} cultivation guidelines."

        primary_risk_factor = causes[0]

        return {
            "crop": crop_clean,
            "location": location_name,
            "weather": {
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall,
                "wind_speed": wind_speed
            },
            "crop_health_score": health_score,
            "health_status": health_status,
            "risk_level": risk_level,
            "primary_risk_factor": primary_risk_factor,
            "agro_climatic_regime": regime_label,
            "causes": causes[:4],  # Top 4 distinct causes
            "precautions": precautions[:4],  # Top 4 actionable precautions
            "ai_explanation": explanation,
            "timestamp": datetime.utcnow().isoformat()
        }
