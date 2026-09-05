"""
Practical 02: Agricultural Risk State Exploration via BFS & DFS
Author: CropGuard AI Team
Description:
    Models crop health degradation pathways as an agricultural state graph.
    Demonstrates Breadth-First Search (shortest path to risk mitigation) and
    Depth-First Search (deep exploratory failure modes) independently.
"""

from collections import deque
import json

# Agricultural State Space Transition Graph
# Each edge represents a transition triggered by meteorological shifts or field interventions.
AGRICULTURAL_RISK_GRAPH = {
    "Healthy_Crop": [
        "Moderate_Drought_Stress",
        "Elevated_Humidity_Alert",
        "Temperature_Anomaly"
    ],
    "Moderate_Drought_Stress": [
        "Severe_Wilting",
        "Controlled_Drip_Irrigation",
        "Nutrient_Deficiency"
    ],
    "Elevated_Humidity_Alert": [
        "Fungal_Spore_Germination",
        "Canopy_Thinning_Intervention",
        "Bacterial_Spot_Outbreak"
    ],
    "Temperature_Anomaly": [
        "Heat_Stress_Senescence",
        "Cold_Stunting",
        "Shade_Net_Mitigation"
    ],
    "Severe_Wilting": [
        "Irreversible_Crop_Failure"
    ],
    "Fungal_Spore_Germination": [
        "Severe_Foliar_Blight",
        "Fungicide_Spray_Intervention"
    ],
    "Bacterial_Spot_Outbreak": [
        "Systemic_Bacterial_Rot"
    ],
    "Heat_Stress_Senescence": [
        "Terminal_Yield_Loss"
    ],
    "Cold_Stunting": [
        "Delayed_Maturity"
    ],
    "Controlled_Drip_Irrigation": [
        "Recovered_Healthy_Crop"
    ],
    "Canopy_Thinning_Intervention": [
        "Recovered_Healthy_Crop"
    ],
    "Shade_Net_Mitigation": [
        "Recovered_Healthy_Crop"
    ],
    "Fungicide_Spray_Intervention": [
        "Recovered_Healthy_Crop"
    ],
    "Irreversible_Crop_Failure": [],
    "Severe_Foliar_Blight": [],
    "Systemic_Bacterial_Rot": [],
    "Terminal_Yield_Loss": [],
    "Delayed_Maturity": [],
    "Recovered_Healthy_Crop": [],
    "Nutrient_Deficiency": ["Recovered_Healthy_Crop"]
}

def breadth_first_search(graph, start_state, goal_state):
    """
    Independent Breadth-First Search (BFS) implementation using a FIFO queue.
    Explores state space level-by-level to guarantee the shortest mitigation path.
    """
    visited = set()
    queue = deque([[start_state]])
    visited.add(start_state)
    traversal_order = []

    while queue:
        path = queue.popleft()
        current_node = path[-1]
        traversal_order.append(current_node)

        if current_node == goal_state:
            return {
                "success": True,
                "algorithm": "BFS",
                "goal_state": goal_state,
                "shortest_path": path,
                "path_cost_steps": len(path) - 1,
                "nodes_expanded": len(traversal_order),
                "traversal_order": traversal_order
            }

        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return {
        "success": False,
        "algorithm": "BFS",
        "goal_state": goal_state,
        "nodes_expanded": len(traversal_order),
        "traversal_order": traversal_order
    }

def depth_first_search(graph, start_state, goal_state):
    """
    Independent Depth-First Search (DFS) implementation using an explicit LIFO stack.
    Explores deep into risk branches before backtracking.
    """
    visited = set()
    stack = [[start_state]]
    traversal_order = []

    while stack:
        path = stack.pop()
        current_node = path[-1]

        if current_node not in visited:
            visited.add(current_node)
            traversal_order.append(current_node)

            if current_node == goal_state:
                return {
                    "success": True,
                    "algorithm": "DFS",
                    "goal_state": goal_state,
                    "path_found": path,
                    "path_cost_steps": len(path) - 1,
                    "nodes_expanded": len(traversal_order),
                    "traversal_order": traversal_order
                }

            # Add neighbors in reverse order to preserve canonical left-to-right branch traversal
            for neighbor in reversed(graph.get(current_node, [])):
                if neighbor not in visited:
                    stack.append(path + [neighbor])

    return {
        "success": False,
        "algorithm": "DFS",
        "goal_state": goal_state,
        "nodes_expanded": len(traversal_order),
        "traversal_order": traversal_order
    }

def run_practical_02():
    print("=" * 60)
    print("PRACTICAL 02: AGRICULTURAL STATE EXPLORATION (BFS & DFS)")
    print("=" * 60)

    start = "Healthy_Crop"
    goal_recovery = "Recovered_Healthy_Crop"
    goal_failure = "Severe_Foliar_Blight"

    print(f"\n[Scenario 1] Finding optimal mitigation recovery path to '{goal_recovery}'")
    bfs_result = breadth_first_search(AGRICULTURAL_RISK_GRAPH, start, goal_recovery)
    print(f"BFS Solution: {' -> '.join(bfs_result['shortest_path'])}")
    print(f"BFS Steps: {bfs_result['path_cost_steps']} | Nodes Expanded: {bfs_result['nodes_expanded']}")

    dfs_result = depth_first_search(AGRICULTURAL_RISK_GRAPH, start, goal_recovery)
    print(f"DFS Solution: {' -> '.join(dfs_result['path_found'])}")
    print(f"DFS Steps: {dfs_result['path_cost_steps']} | Nodes Expanded: {dfs_result['nodes_expanded']}")

    print(f"\n[Scenario 2] Exploring disease escalation pathway to '{goal_failure}'")
    bfs_fail = breadth_first_search(AGRICULTURAL_RISK_GRAPH, start, goal_failure)
    print(f"BFS Disease Escalation: {' -> '.join(bfs_fail['shortest_path'])}")

    dfs_fail = depth_first_search(AGRICULTURAL_RISK_GRAPH, start, goal_failure)
    print(f"DFS Disease Escalation: {' -> '.join(dfs_fail['path_found'])}")

    return bfs_result, dfs_result

if __name__ == "__main__":
    run_practical_02()
