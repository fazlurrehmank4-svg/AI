"""
Practical 04: Local Search Optimization via Hill Climbing for Agricultural Field Management
Author: CropGuard AI Team
Description:
    Implements Steepest-Ascent Hill Climbing, Simple Hill Climbing, and
    Stochastic/Random-Restart Hill Climbing to optimize irrigation rate (mm/day)
    and shade-net coverage (%) to maximize Crop Physiological Comfort (Objective Function).
    Demonstrates state representation, neighborhood generation, local vs. global optima.
"""

import random

class AgriculturalOptimizationEnvironment:
    """
    Models field micro-climate optimization.
    State representation: (irrigation_mm, shade_percent)
    - irrigation_mm: continuous range [0.0 to 40.0] mm/day
    - shade_percent: continuous range [0.0 to 80.0] %
    """
    def __init__(self, crop="Tomato", ambient_temp=34.0, ambient_humidity=38.0):
        self.crop = crop
        self.ambient_temp = ambient_temp
        self.ambient_humidity = ambient_humidity

    def objective_function(self, state):
        """
        Crop Health Comfort Objective Score (0 to 100).
        Evaluates how effectively the irrigation and shade balance canopy heat and transpiration.
        Includes a non-linear multimodal landscape with a local optimum and a global optimum.
        """
        irrigation, shade = state

        # Bounds enforcement
        if not (0 <= irrigation <= 40 and 0 <= shade <= 80):
            return -float("inf")

        # Optimal target for Tomato in high heat:
        # Ideal irrigation: ~24.0 mm, Ideal shade: ~35%
        # Sub-optimal local plateau around irrigation: ~8.0 mm, shade: ~15%
        global_peak = 100.0 - (0.18 * ((irrigation - 24.0) ** 2) + 0.12 * ((shade - 35.0) ** 2))
        local_peak = 72.0 - (0.35 * ((irrigation - 8.0) ** 2) + 0.25 * ((shade - 15.0) ** 2))

        return max(global_peak, local_peak)

    def get_neighbors(self, state, step_size=2.0):
        """
        Generates 8-directional spatial neighbors around current state.
        """
        irrigation, shade = state
        deltas = [-step_size, 0.0, step_size]
        neighbors = []

        for di in deltas:
            for ds in deltas:
                if di == 0.0 and ds == 0.0:
                    continue
                cand_irr = round(max(0.0, min(40.0, irrigation + di)), 1)
                cand_shade = round(max(0.0, min(80.0, shade + ds)), 1)
                neighbors.append((cand_irr, cand_shade))

        return neighbors

def steepest_ascent_hill_climbing(env, initial_state, max_iterations=100):
    """
    Steepest-Ascent Hill Climbing:
    Evaluates all neighbors and moves to the single neighbor with the highest objective score.
    Stops when no neighbor has a higher score (local or global optimum).
    """
    current_state = initial_state
    current_val = env.objective_function(current_state)
    history = [(current_state, current_val)]

    for step in range(max_iterations):
        neighbors = env.get_neighbors(current_state)
        best_neighbor = None
        best_val = current_val

        for n in neighbors:
            score = env.objective_function(n)
            if score > best_val:
                best_val = score
                best_neighbor = n

        # If no neighbor strictly improves objective, reached a peak (local or global)
        if best_neighbor is None or best_val <= current_val:
            break

        current_state = best_neighbor
        current_val = best_val
        history.append((current_state, current_val))

    return {
        "final_state": current_state,
        "optimal_score": round(current_val, 2),
        "steps_taken": len(history) - 1,
        "trajectory": history
    }

def random_restart_hill_climbing(env, num_restarts=5):
    """
    Random-Restart Hill Climbing:
    Executes multiple runs from uniformly distributed random seeds
    to overcome deceptive local optima and locate the global optimum.
    """
    best_overall_state = None
    best_overall_score = -float("inf")
    restart_logs = []

    for r in range(num_restarts):
        start = (round(random.uniform(0, 40), 1), round(random.uniform(0, 80), 1))
        result = steepest_ascent_hill_climbing(env, start)
        restart_logs.append({
            "restart_seed": r + 1,
            "start_state": start,
            "reached_state": result["final_state"],
            "score": result["optimal_score"]
        })

        if result["optimal_score"] > best_overall_score:
            best_overall_score = result["optimal_score"]
            best_overall_state = result["final_state"]

    return {
        "global_best_state": best_overall_state,
        "global_best_score": best_overall_score,
        "restarts": restart_logs
    }

def run_practical_04():
    print("=" * 60)
    print("PRACTICAL 04: LOCAL SEARCH OPTIMIZATION (HILL CLIMBING)")
    print("=" * 60)

    env = AgriculturalOptimizationEnvironment(crop="Tomato", ambient_temp=34.0, ambient_humidity=38.0)

    # 1. Starting near the deceptive local optimum
    sub_optimal_start = (6.0, 12.0)
    print(f"\n[Experiment 1] Steepest-Ascent from {sub_optimal_start} (Near Local Peak):")
    res1 = steepest_ascent_hill_climbing(env, sub_optimal_start)
    print(f"Converged State: Irrigation={res1['final_state'][0]} mm, Shade={res1['final_state'][1]}%")
    print(f"Objective Score: {res1['optimal_score']} / 100 (Trapped at Local Optimum!)")
    print(f"Steps: {res1['steps_taken']}")

    # 2. Starting near the global optimum basin
    global_basin_start = (20.0, 30.0)
    print(f"\n[Experiment 2] Steepest-Ascent from {global_basin_start} (Near Global Basin):")
    res2 = steepest_ascent_hill_climbing(env, global_basin_start)
    print(f"Converged State: Irrigation={res2['final_state'][0]} mm, Shade={res2['final_state'][1]}%")
    print(f"Objective Score: {res2['optimal_score']} / 100 (Global Optimum Reached!)")
    print(f"Steps: {res2['steps_taken']}")

    # 3. Random Restart Hill Climbing to systematically escape local peaks
    random.seed(42)
    print("\n[Experiment 3] Random-Restart Hill Climbing (5 Restarts):")
    rr_res = random_restart_hill_climbing(env, num_restarts=5)
    for r in rr_res["restarts"]:
        print(f"Run {r['restart_seed']}: Start={r['start_state']} -> End={r['reached_state']}, Score={r['score']}")
    print(f"\n=> Absolute Global Solution: State={rr_res['global_best_state']}, Score={rr_res['global_best_score']}")

    return res1, res2, rr_res

if __name__ == "__main__":
    run_practical_04()
