"""
Practical 05: Agricultural Inference Engine using Forward & Backward Chaining
Author: CropGuard AI Team
Description:
    Core reasoning system for agricultural Cause Detection and Precaution Generation.
    - Forward Chaining: Ingests observed meteorological facts and fires domain rules to deduce
      crop risk diagnoses, root causes, and actionable precautions.
    - Backward Chaining: Goal-driven verification answering "Why did the system conclude X?"
      by verifying the chain of constituent conditions.
"""

from typing import List, Dict, Set, Tuple, Any

# Formal Agricultural Expert Rules
# Format: {
#   "id": rule_id,
#   "conditions": [set of required fact tokens],
#   "consequence": deduced_fact,
#   "explanation": scientific rationale,
#   "causes": [list of agronomic causes],
#   "precautions": [list of recommended actions]
# }
AGRICULTURAL_RULES = [
    {
        "id": "RULE_FUNGAL_HIGH",
        "conditions": ["humidity_high", "rainfall_high"],
        "consequence": "fungal_disease_risk_high",
        "explanation": "Prolonged leaf wetness and high relative humidity (>80%) accelerate fungal spore germination.",
        "causes": [
            "Excess moisture lingering on plant canopy foliage",
            "Dense vegetative cover reducing air circulation",
            "Elevated relative humidity coupled with frequent precipitation"
        ],
        "precautions": [
            "Thin lower foliage to enhance ventilation through the canopy",
            "Switch to drip irrigation and suspend overhead sprinkling",
            "Apply prophylactic protective bio-fungicide or copper spray"
        ]
    },
    {
        "id": "RULE_BACTERIAL_BLIGHT",
        "conditions": ["temperature_warm", "humidity_high", "wind_strong"],
        "consequence": "bacterial_leaf_blight_risk",
        "explanation": "Warm humid conditions accompanied by wind-driven rain cause mechanical micro-wounds where bacteria enter.",
        "causes": [
            "Wind-driven rain spreading bacterial exudate across leaves",
            "Micro-abrasions on plant surfaces facilitating pathogen entry",
            "High temperature and atmospheric moisture favoring bacterial proliferation"
        ],
        "precautions": [
            "Disinfect pruning tools between handling plants",
            "Avoid field operations while foliage is physically wet",
            "Apply bactericide sprays if lesions begin expanding"
        ]
    },
    {
        "id": "RULE_HEAT_DROUGHT_STRESS",
        "conditions": ["temperature_high", "humidity_low", "rainfall_low"],
        "consequence": "heat_and_drought_stress_severe",
        "explanation": "High ambient temperatures and dry air elevate vapor pressure deficit, inducing severe plant transpiration shock.",
        "causes": [
            "High evapotranspiration exceeding root water uptake capacity",
            "Soil moisture depletion below temporary wilting point",
            "Intense solar radiation scorching sensitive leaf tissues"
        ],
        "precautions": [
            "Apply organic mulch around root zones to retard soil water evaporation",
            "Schedule irrigations during early morning or evening to minimize evaporative loss",
            "Erect temporary shade-netting or foliar anti-transpirant spray if accessible"
        ]
    },
    {
        "id": "RULE_WATERLOGGING_ROOT_ROT",
        "conditions": ["rainfall_high", "soil_drainage_poor"],
        "consequence": "waterlogging_and_root_rot_risk",
        "explanation": "Excessive standing water asphyxiates rhizosphere roots by displacing soil oxygen.",
        "causes": [
            "Water stagnation exceeding 24 hours in the active root zone",
            "Depleted dissolved oxygen in soil pore spaces",
            "Opportunistic Pythium and Phytophthora water mold proliferation"
        ],
        "precautions": [
            "Open drainage trenches at field perimeters immediately",
            "Refrain from heavy machinery traffic to avoid subsoil compaction",
            "Drench root zone with bio-fungicide once excess water recedes"
        ]
    },
    {
        "id": "RULE_PHYSICAL_LODGING",
        "conditions": ["wind_strong", "rainfall_high"],
        "consequence": "crop_lodging_physical_damage",
        "explanation": "High wind velocities combined with rain-softened topsoil cause tall crops to bend and collapse (lodge).",
        "causes": [
            "Excess wind shear exerting drag force on upper crop stalks",
            "Rain-saturated soil losing root anchorage shear strength",
            "Top-heavy canopies with maturing fruit or grain panicles"
        ],
        "precautions": [
            "Earthing up soil along row ridges to reinforce stalk anchorage",
            "Provide mechanical staking or trellis propping for tall plants",
            "Avoid high nitrogen fertilization that produces weak elongated stems"
        ]
    }
]

class AgriculturalReasoningEngine:
    def __init__(self, rules: List[Dict] = None):
        self.rules = rules or AGRICULTURAL_RULES

    def extract_facts_from_weather(self, temp: float, humidity: float, rainfall: float, wind_speed: float, soil_drainage: str = "normal") -> Set[str]:
        """
        Translates raw quantitative sensor/weather data into discrete semantic facts.
        """
        facts = set()

        # Temperature facts
        if temp >= 32.0:
            facts.add("temperature_high")
        elif temp >= 22.0:
            facts.add("temperature_warm")
        elif temp <= 12.0:
            facts.add("temperature_cold")

        # Humidity facts
        if humidity >= 78.0:
            facts.add("humidity_high")
        elif humidity <= 45.0:
            facts.add("humidity_low")

        # Rainfall facts
        if rainfall >= 100.0:
            facts.add("rainfall_high")
        elif rainfall <= 20.0:
            facts.add("rainfall_low")

        # Wind facts
        if wind_speed >= 28.0:
            facts.add("wind_strong")

        # Soil facts
        if soil_drainage == "poor":
            facts.add("soil_drainage_poor")

        return facts

    def forward_chaining(self, initial_facts: Set[str]) -> Dict[str, Any]:
        """
        Forward Chaining (Data-Driven):
        Applies Modus Ponens repeatedly starting from known facts until no new rules can fire.
        Returns:
            - all deduced facts
            - firing rule IDs
            - consolidated causes
            - prioritized precautions
            - trace log
        """
        known_facts = set(initial_facts)
        fired_rules = []
        deduced_causes = []
        deduced_precautions = []
        trace = []

        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule["id"] in [r["id"] for r in fired_rules]:
                    continue

                # Check if all rule antecedents are satisfied
                if all(cond in known_facts for cond in rule["conditions"]):
                    known_facts.add(rule["consequence"])
                    fired_rules.append(rule)
                    deduced_causes.extend(rule["causes"])
                    deduced_precautions.extend(rule["precautions"])
                    trace.append({
                        "step": len(trace) + 1,
                        "rule_fired": rule["id"],
                        "matched_conditions": rule["conditions"],
                        "consequence": rule["consequence"]
                    })
                    changed = True

        return {
            "initial_facts": list(initial_facts),
            "final_facts": list(known_facts),
            "fired_rules_count": len(fired_rules),
            "fired_rules": [r["id"] for r in fired_rules],
            "causes": list(dict.fromkeys(deduced_causes)),  # Deduplicated preserving order
            "precautions": list(dict.fromkeys(deduced_precautions)),
            "inference_trace": trace
        }

    def backward_chaining(self, target_goal: str, known_facts: Set[str]) -> Tuple[bool, List[str], str]:
        """
        Backward Chaining (Goal-Driven):
        Proves whether target_goal is true given known_facts.
        Recursively queries antecedent conditions and produces an explainable justification.
        Returns: (is_proven, missing_facts, explanation)
        """
        # Base case 1: Goal is already an asserted known fact
        if target_goal in known_facts:
            return True, [], f"Goal '{target_goal}' is directly established by verified observational data."

        # Find candidate rules that conclude this target_goal
        matching_rules = [r for r in self.rules if r["consequence"] == target_goal]
        if not matching_rules:
            return False, [target_goal], f"No agricultural rule exists in the knowledge base to deduce '{target_goal}'."

        for rule in matching_rules:
            all_subgoals_true = True
            missing_conditions = []

            for cond in rule["conditions"]:
                sub_proven, sub_missing, _ = self.backward_chaining(cond, known_facts)
                if not sub_proven:
                    all_subgoals_true = False
                    missing_conditions.extend(sub_missing)

            if all_subgoals_true:
                explanation = (
                    f"Verified '{target_goal}' via {rule['id']}. "
                    f"Required conditions {rule['conditions']} are all satisfied by current observations: {rule['explanation']}"
                )
                return True, [], explanation

        return False, missing_conditions, f"Goal '{target_goal}' could not be proven. Missing required conditions: {list(set(missing_conditions))}."

def run_practical_05():
    print("=" * 60)
    print("PRACTICAL 05: FORWARD & BACKWARD CHAINING REASONING ENGINE")
    print("=" * 60)

    engine = AgriculturalReasoningEngine()

    # Scenario: Hot, rainy, and highly humid monsoon day
    temp = 29.5
    humidity = 88.0
    rainfall = 145.0
    wind_speed = 32.0

    print(f"\n[Observation Input] Temp={temp}°C, Humidity={humidity}%, Rain={rainfall}mm, Wind={wind_speed}km/h")
    facts = engine.extract_facts_from_weather(temp, humidity, rainfall, wind_speed)
    print(f"Extracted Semantic Facts: {sorted(list(facts))}")

    # 1. Forward Chaining
    print("\n--- Running Forward Chaining (Data-Driven Discovery) ---")
    fc_result = engine.forward_chaining(facts)
    print(f"Fired Rules: {fc_result['fired_rules']}")
    print(f"Deduced Risk Conclusions: {[f for f in fc_result['final_facts'] if f not in facts]}")
    print("\n[Identified Root Causes]:")
    for i, c in enumerate(fc_result['causes'], 1):
        print(f"  {i}. {c}")
    print("\n[Actionable Precautions]:")
    for i, p in enumerate(fc_result['precautions'], 1):
        print(f"  {i}. {p}")

    # 2. Backward Chaining (Explainability)
    print("\n--- Running Backward Chaining (Goal Justification) ---")
    goal = "fungal_disease_risk_high"
    proven, missing, explanation = engine.backward_chaining(goal, facts)
    print(f"Query: 'Why is {goal} flagged?'")
    print(f"Proven? {proven}")
    print(f"AI Explanation: {explanation}")

    # Backward chaining test for unproven goal
    goal_unproven = "heat_and_drought_stress_severe"
    proven2, missing2, explanation2 = engine.backward_chaining(goal_unproven, facts)
    print(f"\nQuery: 'Is {goal_unproven} true?'")
    print(f"Proven? {proven2}")
    print(f"AI Explanation: {explanation2}")

    return fc_result, (proven, explanation)

if __name__ == "__main__":
    run_practical_05()
