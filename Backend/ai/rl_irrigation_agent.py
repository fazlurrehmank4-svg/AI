"""
Backend AI Module: Reinforcement Learning Irrigation Policy Engine
-------------------------------------------------------------------
Loads trained tabular Q-learning policy and recommends optimal irrigation
and resource management actions based on farmer telemetry.
"""

import os
import joblib
import numpy as np

# Map descriptive strings to state indices
MOISTURE_MAP = {"low": 0, "optimal": 1, "waterlogged": 2}
WEATHER_MAP = {"dry": 0, "sunny": 0, "moderate": 1, "rainy": 2, "torrential": 2}
STAGE_MAP = {"vegetative": 0, "flowering": 1, "maturation": 2}

ACTION_RECOMMENDATIONS = {
    0: {
        "action": "Do Nothing",
        "detail": "Soil moisture is adequate. No immediate watering required.",
        "icon": "water_drop_outlined"
    },
    1: {
        "action": "Light Irrigation (+20% moisture)",
        "detail": "Apply light watering (approx 10-15 mm) to maintain optimal root zone moisture.",
        "icon": "water_drop"
    },
    2: {
        "action": "Heavy Irrigation (+40% moisture)",
        "detail": "Apply deep irrigation (approx 25-30 mm) to recover from severe moisture deficit.",
        "icon": "shower"
    },
    3: {
        "action": "Apply Fertilizer & Nutrient Irrigation",
        "detail": "Apply fertigation mix. Soil moisture and nutrient uptake are critical at this crop stage.",
        "icon": "eco"
    }
}


class RLIrrigationAgent:
    """Service wrapper for loading and running the trained Q-learning policy."""

    def __init__(self, model_path: str = None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, "saved_models", "q_learning_irrigation.joblib")

        self.model_path = model_path
        self.q_table = None
        self.load_policy()

    def load_policy(self):
        """Load trained Q-table or initialize default heuristic matrix if model missing."""
        if os.path.exists(self.model_path):
            try:
                data = joblib.load(self.model_path)
                self.q_table = data.get("q_table")
            except Exception as e:
                print(f"⚠️ Warning: Could not load RL model from {self.model_path}: {e}")
                self.q_table = None

        if self.q_table is None:
            # Fallback 27x4 default Q-table initializing baseline state-action rules
            self.q_table = np.zeros((27, 4))
            for s in range(27):
                m = s // 9
                if m == 0:  # Low moisture -> prefer light or heavy irrigation
                    self.q_table[s, 1] = 5.0
                    self.q_table[s, 2] = 8.0
                elif m == 1:  # Optimal moisture -> prefer do nothing
                    self.q_table[s, 0] = 10.0
                elif m == 2:  # Waterlogged -> strongly prefer do nothing
                    self.q_table[s, 0] = 12.0
                    self.q_table[s, 2] = -15.0

    def recommend_action(self, soil_moisture_status: str, weather_status: str, crop_stage: str) -> dict:
        """
        Given categorical or numeric sensor conditions, return the Q-optimal action recommendation.
        """
        m = MOISTURE_MAP.get(soil_moisture_status.lower(), 0)
        w = WEATHER_MAP.get(weather_status.lower(), 1)
        s = STAGE_MAP.get(crop_stage.lower(), 0)

        state_id = m * 9 + w * 3 + s
        best_action_id = int(np.argmax(self.q_table[state_id]))
        q_values = self.q_table[state_id].tolist()

        recommendation = ACTION_RECOMMENDATIONS[best_action_id].copy()
        recommendation["action_id"] = best_action_id
        recommendation["state_id"] = state_id
        recommendation["confidence"] = float(round(np.max(q_values) / (np.sum(np.abs(q_values)) + 1e-6) * 100, 1))

        return recommendation
