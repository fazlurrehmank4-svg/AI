# Practical 03: Informed Agricultural Heuristic Search (GBFS & A*)

---

## 1. What Is It?
Practical 03 demonstrates informed search strategies—**Greedy Best-First Search (GBFS)** and **A\* Search**—applied to an agricultural intervention decision graph where nodes represent remediation states and edge weights represent operational costs.

## 2. Why Is It Used?
Uninformed searches (BFS/DFS) cannot distinguish between cheap cultural methods (e.g. canopy thinning, cost = 15) and expensive chemical inputs (cost = 40). Informed algorithms incorporate heuristic estimates $h(n)$ of remaining recovery effort to guide searches cost-effectively.

## 3. How Does It Work?
- **Greedy Best-First Search:**
  $$f(n) = h(n)$$
  Expands the node appearing closest to the goal based solely on the heuristic. While rapid, it is susceptible to local detours and sub-optimal pathways.
- **A\* Search:**
  $$f(n) = g(n) + h(n)$$
  Evaluates total projected path cost by summing known path cost $g(n)$ and admissible heuristic $h(n)$. When $h(n) \le h^*(n)$ (never overestimates true cost), A\* is guaranteed to find the mathematically optimal lowest-cost intervention sequence.

## 4. Inputs & Outputs
- **Input:** Weighted graph `AGRICULTURAL_DECISION_GRAPH`, heuristic dictionary `HEURISTIC_VALUES`, start state, and goal state.
- **Output:** Optimal path, cumulative cost $g(n)$, node expansion count, and step-by-step $f(n)$ traces.

## 5. Time & Space Complexity
- **Time Complexity:** $\mathcal{O}(b^d)$ worst-case, where $b$ is the branching factor and $d$ is solution depth; with an informative heuristic, effective branching factor drops close to 1.
- **Space Complexity:** $\mathcal{O}(b^d)$ to maintain priority queue and closed set.

## 6. Project Connection
A\* serves as CropGuard AI's **Prescription Optimization Engine**, selecting the most cost-effective sequence of agricultural remedies when multiple agronomic interventions are available.

## 7. Important Scientific Note
A\* is **not** the crop health prediction model. It is an informed graph-search algorithm designed to plan minimal-cost corrective agricultural actions once risks are identified.

## 8. Runnable Command
```bash
python Practical_03_GBFS_AStar/gbfs_astar.py
```
