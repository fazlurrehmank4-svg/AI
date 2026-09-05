# Practical 02: Agricultural Risk State Exploration via BFS & DFS

---

## 1. What Is It?
Practical 02 models the agricultural crop vulnerability lifecycle as a directed state graph and implements **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** independently to explore disease evolution and remediation pathways.

## 2. Why Is It Used?
Agricultural risk management requires evaluating state transitions: when weather conditions deviate, how does a crop move from `Healthy` to `Stress`, `Infestation`, or `Recovery`? Search algorithms provide a formal discrete path exploration mechanism.

## 3. How Does It Work?
- **BFS (Queue-based FIFO):** Explores the graph level-by-level. This guarantees finding the shortest intervention pathway (minimum operational steps required to return to `Recovered_Healthy_Crop`).
- **DFS (Stack-based LIFO):** Explores deeply along individual risk branches, uncovering severe worst-case failure trajectories (e.g., `Elevated_Humidity` $\to$ `Fungal_Spore_Germination` $\to$ `Severe_Foliar_Blight`).

## 4. Inputs & Outputs
- **Input:** Directed graph of agricultural states `AGRICULTURAL_RISK_GRAPH`, `start_state`, and `goal_state`.
- **Output:** Execution dictionary containing `shortest_path` / `path_found`, `path_cost_steps`, `nodes_expanded`, and `traversal_order`.

## 5. Time & Space Complexity
- **Time Complexity:** $\mathcal{O}(V + E)$, where $V$ is vertices (states) and $E$ is edges (transitions).
- **Space Complexity:**
  - BFS: $\mathcal{O}(V)$ queue storage (worst case proportional to frontier breadth).
  - DFS: $\mathcal{O}(h)$ stack depth, where $h$ is the maximum path depth.

## 6. Project Connection
Supplies the discrete decision and state-exploration backbone used in CropGuard AI's precautionary pathway logic and interactive decision audits.

## 7. Limitations
Neither BFS nor DFS evaluates numerical transition costs (e.g., financial cost of fungicide vs. drip irrigation) or heuristic proximity; this motivates informed search in Practical 03 (GBFS and A*).

## 8. Runnable Command
```bash
python Practical_02_BFS_DFS/bfs_dfs.py
```
