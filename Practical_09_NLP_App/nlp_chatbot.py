"""
Practical 09: Domain-Specific Agricultural NLP Chatbot (CropGuard AI Assistant)
Author: CropGuard AI Team
Description:
    Local, domain-specific NLP conversational assistant running without external LLMs.
    Pipeline:
      1. Text cleaning, tokenization, synonym normalization, stopword filtering.
      2. TF-IDF vectorization and cosine similarity knowledge retrieval over Kaggle agricultural corpus.
      3. Intent detection: crop requirements, disease etiology, weather risks, precautions.
      4. Context awareness: incorporates active crop & prediction state.
      5. Reasoning Engine coupling: integrates Backward Chaining to answer 'Why this risk?'.
      6. Confidence thresholding: returns honest, conservative advisories for out-of-domain queries.
"""

import os
import re
import json
import math
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Import Practical 05 Reasoning Engine
import sys
sys.path.append(os.path.abspath("Practical_05_Reasoning"))
try:
    from reasoning_engine import AgriculturalReasoningEngine
except ImportError:
    # Fallback if imported from another cwd
    from Practical_05_Reasoning.reasoning_engine import AgriculturalReasoningEngine

# Canonical Synonym & Term Normalization Dictionary
SYNONYM_MAP = {
    "warm": "temperature",
    "hot": "temperature",
    "cold": "temperature",
    "chilly": "temperature",
    "heat": "temperature",
    "degrees": "temperature",
    "moist": "humidity",
    "moisture": "humidity",
    "humid": "humidity",
    "damp": "humidity",
    "rain": "rainfall",
    "precipitation": "rainfall",
    "downpour": "rainfall",
    "rains": "rainfall",
    "windy": "wind",
    "gale": "wind",
    "yellowing": "yellow_leaves",
    "yellow": "yellow_leaves",
    "fungus": "fungal",
    "fungi": "fungal",
    "mold": "fungal",
    "mildew": "fungal",
    "blight": "blight",
    "remedy": "precaution",
    "treatment": "precaution",
    "prevent": "precaution",
    "measure": "precaution",
    "advice": "precaution"
}

STOPWORDS = {
    "a", "about", "above", "after", "again", "all", "am", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself",
    "me", "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same",
    "she", "should", "so", "some", "such", "t", "than", "that", "the", "their", "theirs",
    "them", "themselves", "then", "there", "these", "they", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "we", "were", "what", "when",
    "where", "which", "while", "who", "whom", "why", "will", "with", "you", "your", "yours"
}

# Domain Agricultural Knowledge Corpus for Retrieval
AGRICULTURAL_CORPUS = [
    {
        "topic": "wheat_temperature",
        "crop": "Wheat",
        "query_templates": [
            "what is the best temperature for wheat",
            "optimal temperature for wheat growing",
            "temperature requirements for wheat crop",
            "is high temperature dangerous for wheat",
            "wheat heat tolerance"
        ],
        "answer": "Wheat thrives best in cool to moderate temperatures between 15°C and 25°C. Temperatures exceeding 30°C during the grain-filling stage can trigger terminal heat stress, causing shriveled grains and premature senescence."
    },
    {
        "topic": "rice_conditions",
        "crop": "Rice",
        "query_templates": [
            "what conditions are good for rice",
            "best temperature and humidity for rice",
            "is high temperature dangerous for rice",
            "rice weather requirements",
            "rainfall requirement for paddy rice"
        ],
        "answer": "Rice requires warm and humid conditions, with optimal temperatures between 22°C and 32°C, relative humidity of 70% to 85%, and high rainfall (150-300 mm). Extreme heat (>38°C) during flowering can cause floret sterility."
    },
    {
        "topic": "tomato_temperature_humidity",
        "crop": "Tomato",
        "query_templates": [
            "what is optimal temperature for tomato",
            "tomato humidity range",
            "best weather for growing tomatoes",
            "how does humidity affect tomatoes"
        ],
        "answer": "Tomatoes grow best in warm, moderate conditions with temperatures between 18°C and 28°C and 50% to 70% relative humidity. Humidity above 80% sharply elevates the risk of Early and Late Blight."
    },
    {
        "topic": "high_humidity_impact",
        "crop": "General",
        "query_templates": [
            "what happens if humidity is too high",
            "high humidity problem in crops",
            "humidity is too high what should i do",
            "how does humidity affect crops",
            "what happens when humidity increases"
        ],
        "answer": "High relative humidity (>80%) restricts plant transpiration and maintains persistent leaf wetness, creating ideal germination conditions for fungal pathogens such as blast, rust, and downy mildew. Recommended precautions include thinning dense foliage to improve aeration and avoiding overhead sprinkling."
    },
    {
        "topic": "high_rainfall_flooding",
        "crop": "General",
        "query_templates": [
            "what should i do if rainfall is high",
            "heavy rain damage crops",
            "excess rainfall precautions",
            "how to protect crops from heavy rainfall",
            "flooding waterlogging in field"
        ],
        "answer": "Prolonged high rainfall leads to soil waterlogging and root oxygen starvation. Clear perimeter drainage furrows immediately to evacuate standing water, delay nitrogen top-dressing until soils drain, and monitor for water mold pathogens (Pythium/Phytophthora)."
    },
    {
        "topic": "yellow_leaves_symptom",
        "crop": "General",
        "query_templates": [
            "why are my leaves turning yellow",
            "yellow leaves cause",
            "crop leaves yellowing problem",
            "what causes leaf yellowing"
        ],
        "answer": "Yellowing leaves (chlorosis) in crops typically stems from either: 1) Nitrogen deficiency, 2) Waterlogged roots inhibiting nutrient uptake, or 3) Root rot or viral infection. Inspect the lower leaves first; if accompanied by wet soils, improve drainage and apply light balanced foliar nutrition."
    },
    {
        "topic": "fungal_disease_causes",
        "crop": "General",
        "query_templates": [
            "what causes fungal disease",
            "why are my crops getting fungal problems",
            "fungal infection reasons in plants",
            "how do fungal spores spread"
        ],
        "answer": "Fungal diseases are predominantly driven by the combination of elevated relative humidity (>80%), moderate-to-warm temperatures, and persistent canopy moisture. Spores spread via wind gusts and rain splashes. Ensure optimal plant spacing and apply preventive bio-fungicides."
    },
    {
        "topic": "precautions_general",
        "crop": "General",
        "query_templates": [
            "what precautions should i take",
            "how to protect crop health",
            "general crop protection measures",
            "what should i do to improve crop health"
        ],
        "answer": "To protect and enhance crop health: 1) Maintain proper soil drainage to avert root rot, 2) Scout canopies twice weekly for early lesion spotting, 3) Use drip irrigation rather than overhead sprinklers, and 4) Balance nitrogen fertilizers with phosphorus and potassium to strengthen cell walls."
    },
    {
        "topic": "wind_damage",
        "crop": "General",
        "query_templates": [
            "wind speed effect on crops",
            "strong wind damage protection",
            "crops falling down due to wind lodging"
        ],
        "answer": "High wind speeds (>30 km/h) combined with rain-softened soils cause crop lodging (physical bending/collapse). Earth up soil along rows to reinforce root crowns, install windbreak netting on exposed borders, and stake vulnerable plants."
    },
    {
        "topic": "forecast_harm_next_3_days",
        "crop": "General",
        "query_templates": [
            "will there be any harm to my crop in next 3 days",
            "weather forecast crop risk next 3 days",
            "possible harm to crop in next 3 days",
            "upcoming weather damage to crop",
            "next 3 days weather impact",
            "will rain or heat harm my crop this week",
            "future weather risk for my farm"
        ],
        "answer": "Over the next 3 days, potential crop harm is determined by peak canopy temperatures, precipitation accumulation, and wind gusts. Heavy rainfall (>20mm) triggers root zone waterlogging and fungal sporulation; thermal spikes (>32°C) cause flower abortion and forced grain ripening; while strong winds (>28 km/h) risk physical crop lodging. Consult your 3-Day Forecast Alert tab for daily threat evaluations and tailored precautions."
    },
    {
        "topic": "three_day_weather_precautions",
        "crop": "General",
        "query_templates": [
            "what precautions should i take in next 3 days",
            "precaution for upcoming weather",
            "prevention steps for next 3 days",
            "how to protect crop against 3 day forecast",
            "precautions for weather changes",
            "what precautions should i take"
        ],
        "answer": "Key protective precautions for upcoming 3-day weather shifts: 1) Deepen perimeter and furrow drainage trenches before heavy rainfall begins to avoid waterlogging; 2) Postpone foliar spraying of fertilizers or pesticides during rainy or windy periods to prevent runoff; 3) Under severe heat forecasts, irrigate lightly during early morning or evening hours to insulate roots; 4) Provide earthing-up or staking to support standing crops against wind lodging."
    },
    {
        "topic": "crop_disease_precautions",
        "crop": "General",
        "query_templates": [
            "how to prevent disease in crop",
            "disease prevention precautions",
            "how to protect from fungal attack",
            "precaution against crop disease",
            "prevent fungal blight and rust"
        ],
        "answer": "To prevent weather-induced crop disease: ensure balanced fertilization (avoid excess nitrogen which produces tender, disease-prone tissues), maintain row spacing to encourage canopy air circulation, apply prophylactic biological agents (such as Trichoderma viride) or copper fungicides before prolonged humid rains, and regularly inspect lower leaf surfaces."
    }
]

class LocalFarmerChatbot:
    """
    Local domain-specific agricultural conversational assistant.
    Zero external LLM dependencies.
    """
    def __init__(self, knowledge_base_path="Data/knowledge_base/crop_knowledge.json"):
        self.reasoning_engine = AgriculturalReasoningEngine()
        self.knowledge_base = {}

        if os.path.exists(knowledge_base_path):
            with open(knowledge_base_path, "r") as f:
                self.knowledge_base = json.load(f)

        # Build TF-IDF index over the agricultural knowledge corpus
        self.corpus_entries = []
        self.corpus_documents = []

        for entry in AGRICULTURAL_CORPUS:
            # Combine query templates and answer into searchable representation
            combined_text = " ".join(entry["query_templates"]) + " " + entry["answer"]
            clean_text = self.preprocess_text(combined_text)
            self.corpus_entries.append(entry)
            self.corpus_documents.append(clean_text)

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus_documents)

    def preprocess_text(self, text: str) -> str:
        """
        Tokenization, lowercasing, punctuation removal, synonym mapping, and stopword filtering.
        """
        # Lowercase
        text = text.lower()
        # Remove non-alphanumeric characters
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()

        cleaned_tokens = []
        for t in tokens:
            # Apply synonym normalization
            normalized = SYNONYM_MAP.get(t, t)
            # Filter stopwords
            if normalized not in STOPWORDS and len(normalized) > 1:
                cleaned_tokens.append(normalized)

        return " ".join(cleaned_tokens)

    def detect_crop_in_text(self, text: str) -> Optional[str]:
        """
        Identifies explicit mentions of supported crops.
        """
        text_lower = text.lower()
        supported = ["rice", "wheat", "maize", "cotton", "tomato", "potato", "sugarcane", "chickpea"]
        for crop in supported:
            if crop in text_lower:
                return crop.capitalize()
        return None

    def ask(
        self,
        question: str,
        active_crop: Optional[str] = None,
        current_prediction: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Primary question-answering entrypoint.
        """
        if not question or not question.strip():
            return {
                "answer": "Please enter a specific question regarding your crop or current weather conditions.",
                "confidence": 0.0,
                "matched_topic": "empty_query",
                "category": "system",
                "reasoning_summary": "No input provided."
            }

        cleaned_query = self.preprocess_text(question)
        detected_crop = self.detect_crop_in_text(question) or active_crop

        # -------------------------------------------------------------
        # Branch 1: Context-Aware Prediction Queries
        # e.g. "What should I do?", "Why is my crop at risk?", "Current crop health"
        # -------------------------------------------------------------
        lower_raw = question.lower()
        is_context_query = any(phrase in lower_raw for phrase in [
            "what should i do", "what can i do", "why is my crop at risk",
            "why is risk high", "current crop health", "why this prediction",
            "explain my risk", "how to improve my crop"
        ])

        if is_context_query and current_prediction:
            crop_name = current_prediction.get("crop", detected_crop or "Crop")
            status = current_prediction.get("health_status", "Monitored")
            risk = current_prediction.get("risk_level", "Moderate")
            score = current_prediction.get("crop_health_score", 75.0)
            causes = current_prediction.get("causes", [])
            precautions = current_prediction.get("precautions", [])
            explanation = current_prediction.get("ai_explanation", "")

            # Formulate rich context response
            top_cause = causes[0] if causes else "Weather variations departing from optimal growth envelopes."
            top_precaution = precautions[0] if precautions else "Maintain routine monitoring and ensure adequate field drainage."

            response_text = (
                f"Based on current real-time observations, your {crop_name} is currently assessed at "
                f"**{status}** (Health Score: {score}/100, Risk Level: **{risk}**).\n\n"
                f"• **Key Contributing Cause:** {top_cause}\n"
                f"• **Immediate Recommended Action:** {top_precaution}\n\n"
            )
            if explanation:
                response_text += f"**AI Reasoning Justification:** {explanation}"

            return {
                "answer": response_text,
                "confidence": 0.95,
                "matched_topic": "current_prediction_context",
                "category": "context_prediction",
                "reasoning_summary": f"Synthesized answer using active prediction context for {crop_name}."
            }

        # -------------------------------------------------------------
        # Branch 2: Backward Chaining Specific Query
        # e.g. "Why did you say fungal risk is high?"
        # -------------------------------------------------------------
        if "why" in lower_raw and ("fungal" in lower_raw or "risk" in lower_raw):
            # Check backward chaining with active weather facts if available
            facts = set()
            if current_prediction and "weather" in current_prediction:
                w = current_prediction["weather"]
                facts = self.reasoning_engine.extract_facts_from_weather(
                    w.get("temperature", 25.0),
                    w.get("humidity", 70.0),
                    w.get("rainfall", 50.0),
                    w.get("wind_speed", 10.0)
                )
            else:
                facts = {"humidity_high", "rainfall_high"}

            proven, missing, explanation = self.reasoning_engine.backward_chaining("fungal_disease_risk_high", facts)
            return {
                "answer": f"**Agricultural Rule Justification:**\n{explanation}",
                "confidence": 0.92,
                "matched_topic": "backward_chaining_justification",
                "category": "reasoning",
                "reasoning_summary": "Executed Backward Chaining on fungal_disease_risk_high."
            }

        # -------------------------------------------------------------
        # Branch 3: Crop-Specific Agronomic Knowledge Base Direct Lookup
        # -------------------------------------------------------------
        if detected_crop and detected_crop in self.knowledge_base:
            crop_info = self.knowledge_base[detected_crop]
            # Check if asking for temperature, humidity, rainfall, or diseases
            if any(w in cleaned_query for w in ["temperature", "heat", "cold"]):
                t_min, t_max = crop_info["temp_optimal"]
                return {
                    "answer": f"The optimal temperature envelope for **{detected_crop}** is between **{t_min}°C and {t_max}°C**. Growing conditions outside this range induce thermal stress.",
                    "confidence": 0.90,
                    "matched_topic": f"{detected_crop.lower()}_optimal_temperature",
                    "category": "agronomic_envelope",
                    "reasoning_summary": f"Retrieved optimal temperature bounds for {detected_crop} from structured crop knowledge."
                }
            elif any(w in cleaned_query for w in ["humidity"]):
                h_min, h_max = crop_info["humidity_optimal"]
                return {
                    "answer": f"The optimal relative humidity range for **{detected_crop}** is **{h_min}% to {h_max}%**. Higher humidity can foster fungal pathogens.",
                    "confidence": 0.90,
                    "matched_topic": f"{detected_crop.lower()}_optimal_humidity",
                    "category": "agronomic_envelope",
                    "reasoning_summary": f"Retrieved optimal humidity bounds for {detected_crop}."
                }
            elif any(w in cleaned_query for w in ["rainfall", "rain", "water"]):
                r_min, r_max = crop_info["rainfall_optimal"]
                req = crop_info.get("water_requirement", "Moderate")
                return {
                    "answer": f"**{detected_crop}** requires approximately **{r_min} to {r_max} mm** of precipitation (Water requirement: {req}). Soil: {crop_info.get('soil_type', 'Well-drained loam')}.",
                    "confidence": 0.90,
                    "matched_topic": f"{detected_crop.lower()}_rainfall",
                    "category": "agronomic_envelope",
                    "reasoning_summary": f"Retrieved water/rainfall bounds for {detected_crop}."
                }

        # -------------------------------------------------------------
        # Branch 4: TF-IDF Similarity Retrieval over Agricultural Corpus
        # -------------------------------------------------------------
        if cleaned_query.strip():
            query_vec = self.vectorizer.transform([cleaned_query])
            similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
            best_idx = int(np.argmax(similarities))
            best_score = float(similarities[best_idx])

            # Calibrated confidence threshold (0.22)
            if best_score >= 0.22:
                matched_entry = self.corpus_entries[best_idx]
                confidence_pct = round(min(0.96, best_score * 1.3), 2)
                return {
                    "answer": matched_entry["answer"],
                    "confidence": confidence_pct,
                    "matched_topic": matched_entry["topic"],
                    "category": "retrieval_qa",
                    "reasoning_summary": f"Matched topic '{matched_entry['topic']}' via TF-IDF cosine similarity ({best_score:.3f})."
                }

        # -------------------------------------------------------------
        # Branch 5: Conservative Out-of-Domain Response (No Hallucinations)
        # -------------------------------------------------------------
        return {
            "answer": (
                "I do not have sufficient agricultural knowledge in my local database to answer that question reliably. "
                "As an educational decision-support assistant, I can help you with: "
                "1) Optimal temperature, humidity, and rainfall for supported crops (Rice, Wheat, Maize, Cotton, Tomato, Potato, Sugarcane, Chickpea), "
                "2) High humidity and rainfall risks, 3) Causes of yellow leaves and fungal blights, and 4) Actionable field precautions."
            ),
            "confidence": 0.15,
            "matched_topic": "unsupported_out_of_domain",
            "category": "fallback",
            "reasoning_summary": "Query similarity below threshold (0.22); transparent fallback emitted."
        }

def run_practical_09():
    print("=" * 60)
    print("PRACTICAL 09: LOCAL NLP AGRICULTURAL CHATBOT (ZERO LLM API)")
    print("=" * 60)

    bot = LocalFarmerChatbot()

    test_queries = [
        "What is the best temperature for wheat?",
        "Why are my leaves turning yellow?",
        "What happens if humidity is too high?",
        "What should I do if rainfall is high?",
        "Is high temperature dangerous for rice?",
        "What causes fungal disease?",
        "Why did you say fungal risk is high?",
        "What is the optimal humidity for Tomato?",
        "Can you recommend crypto stocks?"  # Out of domain test
    ]

    for q in test_queries:
        res = bot.ask(q)
        print(f"\nFarmer: \"{q}\"")
        print(f"CropGuard AI ({res['matched_topic']} | Conf: {res['confidence']}):")
        print(f"  {res['answer']}")

    # Context test
    print("\n" + "=" * 50)
    print("[Testing Context-Aware Follow-up with Active Prediction]")
    print("=" * 50)
    mock_prediction = {
        "crop": "Tomato",
        "health_status": "High Risk",
        "risk_level": "High",
        "crop_health_score": 42.0,
        "causes": ["High canopy humidity (>85%) causing foliar moisture saturation."],
        "precautions": ["Improve field airflow, prune dense foliage, and spray copper fungicide."],
        "ai_explanation": "Prolonged high humidity matches conditions for Early and Late Blight."
    }
    context_res = bot.ask("What should I do?", current_prediction=mock_prediction)
    print(f"Farmer: \"What should I do?\" [Context: Tomato High Risk]")
    print(f"CropGuard AI:\n{context_res['answer']}")

    return bot

if __name__ == "__main__":
    run_practical_09()
