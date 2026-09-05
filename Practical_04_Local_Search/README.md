# Practical 04: Local Search Optimization via Hill Climbing

---

## 1. What Is It?
Practical 04 formulates agricultural micro-climate conditioning (balancing irrigation volume and canopy shade percentage) as an unconstrained mathematical optimization problem solved through **Hill Climbing local search algorithms**.

## 2. Why Is It Used?
Field managers face combinatorial continuous tuning dilemmas: under extreme weather anomalies (e.g. $34^\circ\text{C}$ ambient heat), what exact irrigation and protective shade levels maximize crop physiological comfort while minimizing resource waste?

## 3. How Does It Work?
- **State Representation:** A 2-tuple `(irrigation_mm, shade_percent)` within valid biological bounds.
- **Objective Function:** Physiological Comfort Score (0 to 100), modeled with a multi-modal response landscape featuring both an inferior local peak and a global optimum.
- **Neighborhood Operator:** Evaluates 8 spatial perturbations $(\Delta i, \Delta s) \in \{-2, 0, 2\}$.
- **Steepest Ascent:** Moves directly to the highest neighboring score until no strictly superior neighbor exists.
- **Random-Restart:** Executes independent trials from randomly generated initial coordinates to overcome local traps and discover the global maximum.

## 4. Inputs & Outputs
- **Input:** Initial agricultural configuration state `(irrigation_mm, shade_percent)` and objective environment specifications.
- **Output:** Converged optimal state tuple, objective score achieved, convergence trajectory, and restart comparison logs.

## 5. Time & Space Complexity
- **Time Complexity:** $\mathcal{O}(K \times \text{neighbors})$ where $K$ is the number of ascent steps until a ridge or peak is reached (typically $< 25$ iterations).
- **Space Complexity:** $\mathcal{O}(1)$ memory beyond storing the current and neighboring state coordinates.

## 6. Project Connection
Integrates into CropGuard AI's **Microclimate Recommendation Module**, computing continuous resource adjustments when farmers ask how to mitigate temperature or drought anomalies.

## 7. Limitations
Standard Hill Climbing is vulnerable to local maxima, ridges, and plateaus; random restarts or simulated annealing are necessary for robust global convergence.

## 8. Runnable Command
```bash
python Practical_04_Local_Search/hill_climbing.py
```
