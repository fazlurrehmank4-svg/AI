# Practical 04: Local Search Optimization (Hill Climbing & Simulated Annealing)

---

## 1. What Is It?
Practical 04 formulates agricultural micro-climate conditioning (balancing irrigation volume and canopy shade percentage) as an optimization problem solved through **Hill Climbing (Steepest-Ascent, Random-Restart)** and **Simulated Annealing** local search algorithms.

## 2. Why Is It Used?
Field managers face combinatorial continuous tuning dilemmas: under extreme weather anomalies (e.g. $34^\circ\text{C}$ ambient heat), what exact irrigation and protective shade levels maximize crop physiological comfort while minimizing resource waste?

## 3. How Does It Work?
- **State Representation:** A 2-tuple `(irrigation_mm, shade_percent)` within valid biological bounds.
- **Objective Function:** Physiological Comfort Score (0 to 100), modeled with a multi-modal response landscape featuring both an inferior local peak and a global optimum.
- **Neighborhood Operator:** Evaluates spatial perturbations $(\Delta i, \Delta s) \in \{-2, 0, 2\}$.
- **Steepest Ascent:** Moves directly to the highest neighboring score until no strictly superior neighbor exists.
- **Random-Restart:** Executes independent trials from randomly generated initial coordinates to overcome local traps and discover the global maximum.
- **Simulated Annealing:** Uses a cooling temperature schedule $T$ and the Metropolis Acceptance Criterion $P = \exp(\Delta E / T)$ to probabilistically accept temporary sub-optimal moves and break free from deceptive local maxima.

## 4. Inputs & Outputs
- **Input:** Initial agricultural configuration state `(irrigation_mm, shade_percent)` and objective environment specifications.
- **Output:** Converged optimal state tuple, objective score achieved, convergence trajectory, and restart/annealing logs.

## 5. Time & Space Complexity
- **Time Complexity:** $\mathcal{O}(K \times \text{neighbors})$ where $K$ is the number of search steps until peak or minimum temperature is reached.
- **Space Complexity:** $\mathcal{O}(1)$ memory beyond storing current and candidate state coordinates.

## 6. Project Connection
Integrates into CropGuard AI's **Microclimate Recommendation Module**, computing continuous resource adjustments when farmers ask how to mitigate temperature or drought anomalies.

## 7. Limitations
Standard Hill Climbing can be trapped at local maxima; Simulated Annealing and Random-Restarts overcome these limitations by introducing stochastic exploration.

## 8. Runnable Command
```bash
python Practical_04_Local_Search/hill_climbing.py
```
