"""
Practical 03: Agricultural Intervention Planning using Greedy Best-First Search & A* Search
Author: CropGuard AI Team
Description:
    Demonstrates informed heuristic search algorithms (GBFS and A*) on a weighted
    agricultural decision graph. Calculates exact g(n) actual cost, h(n) heuristic
    estimate, and f(n) evaluation function to find the most resource-efficient
    crop recovery path.
"""

import heapq

# Weighted Agricultural Action Graph
# Adjacency list: node -> list of tuples (neighbor, actual_action_cost g)
# Costs represent estimated labor and operational expense units ($ or labor hours)
AGRICULTURAL_DECISION_GRAPH = {
    "Severe_Fungal_Outbreak": [
        ("Chemical_Fungicide", 40),
        ("Organic_Neem_Extract", 25),
        ("Foliage_Canopy_Pruning", 15)
    ],
    "Organic_Neem_Extract": [
        ("Bio_Stimulant_Spray", 20),
        ("Soil_Solarization", 45)
    ],
    "Foliage_Canopy_Pruning": [
        ("Aeration_Improvement", 10),
        ("Bio_Stimulant_Spray", 25)
    ],
    "Chemical_Fungicide": [
        ("Post_Treatment_Quarantine", 30),
        ("Targeted_Leaf_Wash", 15)
    ],
    "Aeration_Improvement": [
        ("Optimal_Microclimate_Restored", 12)
    ],
    "Bio_Stimulant_Spray": [
        ("Optimal_Microclimate_Restored", 18)
    ],
    "Post_Treatment_Quarantine": [
        ("Optimal_Microclimate_Restored", 10)
    ],
    "Targeted_Leaf_Wash": [
        ("Optimal_Microclimate_Restored", 22)
    ],
    "Soil_Solarization": [
        ("Optimal_Microclimate_Restored", 35)
    ],
    "Optimal_Microclimate_Restored": []
}

# Admissible & Consistent Heuristics: h(n)
# Estimated remaining intervention cost to achieve 'Optimal_Microclimate_Restored'
HEURISTIC_VALUES = {
    "Severe_Fungal_Outbreak": 35,
    "Chemical_Fungicide": 25,
    "Organic_Neem_Extract": 22,
    "Foliage_Canopy_Pruning": 18,
    "Aeration_Improvement": 10,
    "Bio_Stimulant_Spray": 15,
    "Post_Treatment_Quarantine": 8,
    "Targeted_Leaf_Wash": 18,
    "Soil_Solarization": 30,
    "Optimal_Microclimate_Restored": 0
}

def greedy_best_first_search(graph, heuristics, start, goal):
    """
    Greedy Best-First Search evaluates nodes solely on heuristic estimate:
    f(n) = h(n).
    Can be sub-optimal because it disregards accrued path cost g(n).
    """
    priority_queue = [(heuristics[start], start, [start], 0)]
    visited = set()
    expansion_trace = []

    while priority_queue:
        h_cost, current_node, path, g_cost = heapq.heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)
        expansion_trace.append({
            "node": current_node,
            "f(n) = h(n)": h_cost,
            "actual_g(n)": g_cost
        })

        if current_node == goal:
            return {
                "algorithm": "Greedy Best-First Search",
                "optimal": False,
                "path": path,
                "total_actual_cost_g": g_cost,
                "nodes_expanded": len(expansion_trace),
                "expansion_trace": expansion_trace
            }

        for neighbor, edge_weight in graph.get(current_node, []):
            if neighbor not in visited:
                heapq.heappush(
                    priority_queue,
                    (heuristics.get(neighbor, 0), neighbor, path + [neighbor], g_cost + edge_weight)
                )

    return {"algorithm": "Greedy Best-First Search", "path": None, "total_actual_cost_g": float("inf")}

def a_star_search(graph, heuristics, start, goal):
    """
    A* Search evaluates nodes using total estimated cost:
    f(n) = g(n) + h(n).
    Since h(n) is admissible (never overestimates remaining cost), A* is guaranteed optimal.
    """
    # Item in heap: (f(n), g(n), current_node, path)
    initial_f = 0 + heuristics[start]
    priority_queue = [(initial_f, 0, start, [start])]
    visited_costs = {}
    expansion_trace = []

    while priority_queue:
        f_cost, g_cost, current_node, path = heapq.heappop(priority_queue)

        if current_node in visited_costs and visited_costs[current_node] <= g_cost:
            continue
        visited_costs[current_node] = g_cost

        h_val = heuristics.get(current_node, 0)
        expansion_trace.append({
            "node": current_node,
            "g(n)": g_cost,
            "h(n)": h_val,
            "f(n) = g(n) + h(n)": f_cost
        })

        if current_node == goal:
            return {
                "algorithm": "A* Search",
                "optimal": True,
                "path": path,
                "total_actual_cost_g": g_cost,
                "nodes_expanded": len(expansion_trace),
                "expansion_trace": expansion_trace
            }

        for neighbor, edge_weight in graph.get(current_node, []):
            new_g = g_cost + edge_weight
            new_h = heuristics.get(neighbor, 0)
            new_f = new_g + new_h
            if neighbor not in visited_costs or new_g < visited_costs[neighbor]:
                heapq.heappush(priority_queue, (new_f, new_g, neighbor, path + [neighbor]))

    return {"algorithm": "A* Search", "path": None, "total_actual_cost_g": float("inf")}

def run_practical_03():
    print("=" * 60)
    print("PRACTICAL 03: INFORMED HEURISTIC SEARCH (GBFS & A*)")
    print("=" * 60)

    start_node = "Severe_Fungal_Outbreak"
    goal_node = "Optimal_Microclimate_Restored"

    print(f"\nEvaluating Agricultural Remediation from '{start_node}' to '{goal_node}':")

    # 1. Greedy Best-First Search
    gbfs_res = greedy_best_first_search(AGRICULTURAL_DECISION_GRAPH, HEURISTIC_VALUES, start_node, goal_node)
    print("\n--- Greedy Best-First Search ---")
    print(f"Path: {' -> '.join(gbfs_res['path'])}")
    print(f"Total Actual Intervention Cost g(n): {gbfs_res['total_actual_cost_g']}")
    print(f"Nodes Expanded: {gbfs_res['nodes_expanded']}")

    # 2. A* Search
    astar_res = a_star_search(AGRICULTURAL_DECISION_GRAPH, HEURISTIC_VALUES, start_node, goal_node)
    print("\n--- A* Search (Guaranteed Cost-Optimal) ---")
    print(f"Path: {' -> '.join(astar_res['path'])}")
    print(f"Total Actual Intervention Cost g(n): {astar_res['total_actual_cost_g']}")
    print(f"Nodes Expanded: {astar_res['nodes_expanded']}")

    print("\n--- Detailed A* Step-by-Step f(n) = g(n) + h(n) Trace ---")
    for step in astar_res["expansion_trace"]:
        print(f"Node: {step['node']:<30} | g(n)={step['g(n)']:<3} | h(n)={step['h(n)']:<3} | f(n)={step['f(n) = g(n) + h(n)']}")

    return gbfs_res, astar_res

if __name__ == "__main__":
    run_practical_03()
