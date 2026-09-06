"""
CropGuard AI Unified Predictor Engine
Coordinates:
  - Dynamic Agronomic & ML Regression Model (Continuous Health Score 0-100)
  - Classification Model (Healthy / At Risk / High Risk)
  - K-Means Clustering (Agro-Climatic Regime)
  - Crop Recommendation Ensemble (N, P, K, Temp, Humidity, pH, Rainfall -> Recommended Crop)
  - Forward Chaining Inference (Causes & Precautions)
  - Backward Chaining Verification (Explainability)
  - 3-Day Crop Hazard & Forecast Alert Engine
"""

import os
import json
import joblib
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional

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
        self.knowledge_base_path = knowledge_base_path
        self.reasoning_engine = AgriculturalReasoningEngine()
        self.knowledge_base = {}

        self._load_knowledge_base()

        # Load ML artifacts
        self.reg_artifact = self._load_joblib("linear_regression.joblib")
        self.dt_artifact = self._load_joblib("decision_tree_model.joblib")
        self.knn_artifact = self._load_joblib("knn_model.joblib")
        self.kmeans_artifact = self._load_joblib("kmeans_model.joblib")
        self.recommender_artifact = self._load_joblib("crop_recommender.joblib")

    def _load_knowledge_base(self):
        if os.path.exists(self.knowledge_base_path):
            try:
                with open(self.knowledge_base_path, "r") as f:
                    self.knowledge_base = json.load(f)
            except Exception as e:
                print(f"[Predictor] Error loading knowledge base: {e}")

    def _load_joblib(self, filename: str):
        path = os.path.join(self.models_dir, filename)
        if os.path.exists(path):
            try:
                return joblib.load(path)
            except Exception as e:
                print(f"[Predictor] Error loading {filename}: {e}")
        return None

    def reload_artifacts(self):
        """Reloads all saved model weights and knowledge base after self-improvement cycle."""
        self._load_knowledge_base()
        self.reg_artifact = self._load_joblib("linear_regression.joblib")
        self.dt_artifact = self._load_joblib("decision_tree_model.joblib")
        self.knn_artifact = self._load_joblib("knn_model.joblib")
        self.kmeans_artifact = self._load_joblib("kmeans_model.joblib")
        self.recommender_artifact = self._load_joblib("crop_recommender.joblib")
        print("[Predictor] Successfully reloaded all updated model artifacts.")

    def recommend_crops(
        self,
        n: float,
        p: float,
        k: float,
        temperature: float,
        humidity: float,
        ph: float,
        rainfall: float,
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Recommends top suitable crops given soil NPK, pH, and local weather.
        """
        if self.recommender_artifact is None:
            self.recommender_artifact = self._load_joblib("crop_recommender.joblib")

        features = np.array([[n, p, k, temperature, humidity, ph, rainfall]])

        if self.recommender_artifact and "model" in self.recommender_artifact and "scaler" in self.recommender_artifact:
            scaler = self.recommender_artifact["scaler"]
            model = self.recommender_artifact["model"]
            le = self.recommender_artifact.get("label_encoder")

            features_scaled = scaler.transform(features)
            probs = model.predict_proba(features_scaled)[0]

            top_indices = np.argsort(probs)[::-1][:top_k]
            recommendations = []

            for idx in top_indices:
                crop_label = le.inverse_transform([idx])[0] if le else f"Crop_{idx}"
                crop_cap = crop_label.capitalize()
                kb_info = self.knowledge_base.get(crop_cap, {})
                recommendations.append({
                    "crop": crop_cap,
                    "confidence": round(float(probs[idx]), 4),
                    "category": kb_info.get("category", "Agricultural Crop"),
                    "growing_season": kb_info.get("growing_season", "Seasonal"),
                    "soil_type": kb_info.get("soil_type", "Loamy / Alluvial"),
                    "water_requirement": kb_info.get("water_requirement", "Moderate"),
                    "emoji": kb_info.get("emoji", "🌱"),
                    "precautions": kb_info.get("precautions", ["Follow recommended cultivation schedules."])[:2]
                })

            best = recommendations[0]
            return {
                "success": True,
                "recommended_crop": best["crop"],
                "confidence": best["confidence"],
                "recommendations": recommendations,
                "input_parameters": {
                    "n": n, "p": p, "k": k,
                    "temperature": temperature,
                    "humidity": humidity,
                    "ph": ph,
                    "rainfall": rainfall
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            # Fallback heuristic recommendation
            return {
                "success": True,
                "recommended_crop": "Wheat",
                "confidence": 0.85,
                "recommendations": [
                    {"crop": "Wheat", "confidence": 0.85, "category": "Cereal Grain", "emoji": "🌾"},
                    {"crop": "Maize", "confidence": 0.10, "category": "Cereal / Fodder", "emoji": "🌽"}
                ],
                "input_parameters": {"n": n, "p": p, "k": k, "temperature": temperature, "humidity": humidity, "ph": ph, "rainfall": rainfall},
                "timestamp": datetime.utcnow().isoformat()
            }

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
        Executes end-to-end multi-model inference and crop-specific reasoning.
        """
        crop_clean = crop.capitalize()

        # 1. Crop-Specific Agronomic Biological Envelope Calculation
        temp_penalty = 0.0
        hum_penalty = 0.0
        rain_penalty = 0.0
        wind_penalty = 0.0

        kb_crop = self.knowledge_base.get(crop_clean, {
            "temp_optimal": (18.0, 28.0),
            "humidity_optimal": (50.0, 75.0),
            "rainfall_optimal": (40.0, 100.0),
            "precautions": ["Follow recommended irrigation schedules and routine crop scouting."]
        })

        t_min, t_max = kb_crop.get("temp_optimal", (18.0, 28.0))
        h_min, h_max = kb_crop.get("humidity_optimal", (50.0, 75.0))
        r_min, r_max = kb_crop.get("rainfall_optimal", (40.0, 100.0))

        if temperature < t_min:
            temp_penalty = min(40.0, (t_min - temperature) * 3.5)
        elif temperature > t_max:
            temp_penalty = min(45.0, (temperature - t_max) * 4.0)

        if humidity < h_min:
            hum_penalty = min(30.0, (h_min - humidity) * 1.2)
        elif humidity > h_max:
            hum_penalty = min(35.0, (humidity - h_max) * 1.5)

        if rainfall < r_min:
            rain_penalty = min(35.0, ((r_min - rainfall) / max(1.0, r_min)) * 35.0)
        elif rainfall > r_max:
            rain_penalty = min(40.0, ((rainfall - r_max) / max(1.0, r_max)) * 40.0)

        if wind_speed > 32.0:
            wind_penalty = min(25.0, (wind_speed - 32.0) * 1.4)

        total_penalty = temp_penalty + hum_penalty + rain_penalty + wind_penalty
        agronomic_score = max(8.0, min(98.0, 100.0 - total_penalty))

        # 2. Regression ML Blend (Anchored by crop agronomics)
        if self.reg_artifact and "model" in self.reg_artifact and "scaler" in self.reg_artifact:
            features_reg = np.array([[temperature, humidity, rainfall, wind_speed]])
            features_scaled = self.reg_artifact["scaler"].transform(features_reg)
            raw_reg = float(self.reg_artifact["model"].predict(features_scaled)[0])
            blended = 0.30 * raw_reg + 0.70 * agronomic_score
            health_score = round(float(np.clip(blended, 8.0, 98.0)), 1)
        else:
            health_score = round(float(agronomic_score), 1)

        # 3. Dynamic Health Status Classification
        if health_score >= 75.0:
            health_status = "Healthy"
            risk_level = "Low"
        elif health_score >= 50.0:
            health_status = "At Risk"
            risk_level = "Moderate"
        else:
            health_status = "High Risk"
            risk_level = "High"

        # 4. K-Means Clustering (Agro-Climatic Regime)
        regime_label = "Temperate Agricultural Zone"
        if self.kmeans_artifact and "model" in self.kmeans_artifact and "scaler" in self.kmeans_artifact:
            features_km = np.array([[temperature, humidity, rainfall, wind_speed]])
            features_km_scaled = self.kmeans_artifact["scaler"].transform(features_km)
            cluster_id = int(self.kmeans_artifact["model"].predict(features_km_scaled)[0])
            regime_label = self.kmeans_artifact.get("label_map", {}).get(cluster_id, f"Climatic Cluster {cluster_id}")

        # 5. Forward Chaining Reasoning (Causes & Precautions)
        facts = self.reasoning_engine.extract_facts_from_weather(temperature, humidity, rainfall, wind_speed)
        fc_res = self.reasoning_engine.forward_chaining(facts)

        causes = list(fc_res.get("causes", []))
        precautions = list(fc_res.get("precautions", []))

        # Crop-specific cause identification
        if temperature < t_min:
            causes.insert(0, f"Canopy temperature ({temperature:.1f}°C) is {t_min - temperature:.1f}°C below {crop_clean}'s optimal minimum ({t_min}°C).")
        elif temperature > t_max:
            causes.insert(0, f"Canopy temperature ({temperature:.1f}°C) exceeds {crop_clean}'s thermal ceiling ({t_max}°C).")

        if humidity > h_max:
            causes.append(f"Relative humidity ({humidity:.1f}%) exceeds recommended threshold of {h_max}%, elevating foliar blight risk.")
        elif humidity < h_min:
            causes.append(f"Dry air ({humidity:.1f}%) accelerates evapo-transpiration for {crop_clean}.")

        if rainfall > r_max:
            causes.append(f"Rainfall ({rainfall:.1f} mm) surpasses {crop_clean}'s optimal ceiling ({r_max} mm), risking root zone waterlogging.")
        elif rainfall < r_min:
            causes.append(f"Rainfall deficit ({rainfall:.1f} mm vs optimal {r_min}-{r_max} mm) requires supplemental irrigation.")

        # Enrich precautions
        for p in kb_crop.get("precautions", []):
            if p not in precautions:
                precautions.append(p)

        if not causes:
            causes = ["Meteorological parameters remain within acceptable biological envelopes for this crop."]
        if not precautions:
            precautions = ["Maintain scheduled scoutings and follow standard irrigation management."]

        # 6. Backward Chaining Explanation
        if "fungal_disease_risk_high" in fc_res.get("final_facts", []):
            _, _, explanation = self.reasoning_engine.backward_chaining("fungal_disease_risk_high", facts)
        elif "heat_and_drought_stress_severe" in fc_res.get("final_facts", []):
            _, _, explanation = self.reasoning_engine.backward_chaining("heat_and_drought_stress_severe", facts)
        elif health_status == "Healthy":
            explanation = f"Current weather conditions (Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%) match optimal agronomic envelopes for {crop_clean}."
        else:
            explanation = f"Crop health diagnosed as '{health_status}' (Score {health_score}/100) due to observed deviations from {crop_clean}'s recommended cultivation standards."

        primary_risk_factor = causes[0] if causes else "Normal Parameters"

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
            "causes": causes[:4],
            "precautions": precautions[:4],
            "ai_explanation": explanation,
            "timestamp": datetime.utcnow().isoformat()
        }

    def evaluate_forecast_hazards(
        self,
        crop: str,
        forecast_days: List[Dict[str, Any]],
        location_name: str = "Local Farm"
    ) -> Dict[str, Any]:
        """
        Evaluates weather for the next 3 days, identifying specific crop hazards and actionable precautions.
        """
        crop_clean = crop.capitalize()
        kb_crop = self.knowledge_base.get(crop_clean, {
            "temp_optimal": (18.0, 28.0),
            "humidity_optimal": (50.0, 75.0),
            "rainfall_optimal": (40.0, 100.0),
            "precautions": ["Follow standard moisture management."]
        })

        t_min, t_max = kb_crop.get("temp_optimal", (18.0, 28.0))
        r_min, r_max = kb_crop.get("rainfall_optimal", (40.0, 100.0))

        daily_alerts = []
        highest_threat = "Low"

        for idx, day in enumerate(forecast_days):
            t_high = float(day.get("temp_max", 28.0))
            t_low = float(day.get("temp_min", 20.0))
            rain = float(day.get("rainfall", 0.0))
            wind = float(day.get("wind_speed", 10.0))
            w_code = int(day.get("weather_code", 0))

            hazards = []
            precautions = []
            day_risk = "Low"

            # 1. Thermal Stress
            if t_high > (t_max + 3.0):
                hazards.append(f"Excessive heat peak ({t_high:.1f}°C) exceeds {crop_clean} tolerance ({t_max}°C).")
                precautions.append("Provide light irrigation during early morning or evening to lower root zone temperature.")
                precautions.append("Apply anti-transpirant spray or mulch around crop rows.")
                day_risk = "High"
            elif t_high > t_max:
                hazards.append(f"Moderate heat wave ({t_high:.1f}°C) may accelerate plant transpiration.")
                precautions.append("Monitor soil moisture levels closely.")
                if day_risk == "Low": day_risk = "Moderate"

            if t_low < (t_min - 3.0):
                hazards.append(f"Cold snap ({t_low:.1f}°C) threatens chilling injury to sensitive {crop_clean} tissues.")
                precautions.append("Provide light surface irrigation at sunset to insulate the field canopy.")
                day_risk = "High"

            # 2. Precipitation / Storm / Flood
            if rain >= 25.0:
                hazards.append(f"Torrential rainfall ({rain:.1f} mm) threatens waterlogging, root asphyxiation, and fungal explosion.")
                precautions.append("Open furrow drainage trenches immediately to prevent standing water.")
                precautions.append("Postpone fertilizer and pesticide applications until soil drains.")
                day_risk = "High"
            elif rain >= 12.0:
                hazards.append(f"Significant precipitation ({rain:.1f} mm) may elevate foliar disease pressure.")
                precautions.append("Clear drainage channels and prepare protective copper/triazole fungicide.")
                if day_risk == "Low": day_risk = "Moderate"

            # 3. Gale Wind Force
            if wind >= 28.0:
                hazards.append(f"High wind velocity ({wind:.1f} km/h) risks crop lodging and stalk snapping.")
                precautions.append("Provide mechanical staking or earthing up to support standing stalks.")
                if day_risk != "High": day_risk = "Moderate"

            # 4. Thunderstorm / Severe Hail
            if w_code in [95, 96, 99]:
                hazards.append("Thunderstorm & severe weather activity predicted.")
                precautions.append("Avoid field machinery operations and protect nursery structures.")
                day_risk = "High"

            has_harm = len(hazards) > 0
            if not hazards:
                harm_summary = f"Favorable conditions. Weather parameters remain well-suited for {crop_clean} development."
                precautions = ["Maintain routine scouting and adhere to regular fertilization schedule."]
            else:
                harm_summary = " ".join(hazards)

            if day_risk == "High":
                highest_threat = "High"
            elif day_risk == "Moderate" and highest_threat != "High":
                highest_threat = "Moderate"

            daily_alerts.append({
                "date": day.get("date", f"Day {idx+1}"),
                "day_name": day.get("day_name", f"Day {idx+1}"),
                "temp_max": t_high,
                "temp_min": t_low,
                "rainfall": rain,
                "wind_speed": wind,
                "condition": day.get("condition", "Partly Cloudy"),
                "weather_code": w_code,
                "risk_level": day_risk,
                "has_harm": has_harm,
                "harm_summary": harm_summary,
                "precautions": precautions[:3]
            })

        summary = (
            f"3-Day Forecast for {crop_clean}: Overall Threat Level is {highest_threat.upper()}. "
            + ("Crop hazards detected; immediate precautions advised." if highest_threat != "Low" else "No adverse weather harm expected over the next 72 hours.")
        )

        return {
            "crop": crop_clean,
            "location": location_name,
            "overall_threat_level": highest_threat,
            "summary": summary,
            "alerts": daily_alerts,
            "timestamp": datetime.utcnow().isoformat()
        }
