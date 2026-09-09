"""
Practical 11: Reinforcement Learning (Q-Learning for Optimal Crop Irrigation)
--------------------------------------------------------------------------------
CropGuard AI - Agricultural Decision Support System

This script implements a Markov Decision Process (MDP) environment simulating crop soil dynamics
and a Tabular Q-Learning Agent that learns an optimal dynamic policy for irrigation and resource allocation.

Key Concepts Demonstrated:
1. Environment Modeling (State space, Action space, Transition dynamics, Reward structure)
2. Q-Learning Algorithm (Temporal Difference error, Bellman Optimality Equation)
3. Exploration vs. Exploitation (Epsilon-Greedy policy with decay)
4. Policy Evaluation & Convergence Visualization
"""

import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Discrete State Definitions
MOISTURE_LEVELS = ["Low (<30%)", "Optimal (30-70%)", "Waterlogged (>70%)"]  # 0, 1, 2
WEATHER_CONDITIONS = ["Dry/Sunny", "Moderate", "Torrential Rain"]            # 0, 1, 2
CROP_STAGES = ["Vegetative", "Flowering", "Yield Maturation"]                # 0, 1, 2

# Action Definitions
ACTIONS = [
    "0: Do Nothing",
    "1: Light Irrigation (+20% moisture)",
    "2: Heavy Irrigation (+40% moisture)",
    "3: Apply Nutrient Irrigation"
]

NUM_STATES = len(MOISTURE_LEVELS) * len(WEATHER_CONDITIONS) * len(CROP_STAGES) # 27 States
NUM_ACTIONS = len(ACTIONS) # 4 Actions


def encode_state(moisture: int, weather: int, stage: int) -> int:
    """Encode discrete state variables into a unique integer state ID (0 to 26)."""
    return moisture * 9 + weather * 3 + stage


def decode_state(state_id: int) -> tuple[int, int, int]:
    """Decode integer state ID back into (moisture, weather, stage) tuple."""
    moisture = state_id // 9
    rem = state_id % 9
    weather = rem // 3
    stage = rem % 3
    return moisture, weather, stage


class CropIrrigationEnv:
    """
    Simulated Agricultural Environment (Markov Decision Process).
    Tracks soil moisture, weather shifts, and crop development stages over a 30-day crop cycle.
    """

    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        self.reset()

    def reset(self):
        """Reset environment state to start of crop cycle."""
        self.day = 1
        self.max_days = 30
        self.moisture = 0  # Starts Low
        self.weather = random.choice([0, 1])  # Dry or Moderate
        self.stage = 0  # Vegetative stage
        self.crop_health = 70.0
        return encode_state(self.moisture, self.weather, self.stage)

    def step(self, action: int) -> tuple[int, float, bool, dict]:
        """
        Execute one action in the environment and return (next_state, reward, done, info).
        """
        reward = 0.0

        # Action cost/penalty
        if action == 0:
            reward -= 0.0  # Free
        elif action == 1:
            reward -= 1.0  # Small water cost
        elif action == 2:
            reward -= 3.0  # High water cost
        elif action == 3:
            reward -= 4.0  # Fertilizer + water cost

        # Apply action effect on moisture
        new_moisture = self.moisture
        if action == 1:
            new_moisture = min(2, new_moisture + 1)
        elif action == 2 or action == 3:
            new_moisture = min(2, new_moisture + 2)

        # Environment dynamics (Weather impact)
        next_weather = np.random.choice([0, 1, 2], p=[0.5, 0.35, 0.15])
        if next_weather == 0:  # Dry weather depletes moisture
            new_moisture = max(0, new_moisture - 1)
        elif next_weather == 2:  # Heavy rain floods soil
            new_moisture = min(2, new_moisture + 1)

        self.moisture = new_moisture
        self.weather = next_weather

        # Update crop development stage every 10 days
        self.day += 1
        if self.day <= 10:
            self.stage = 0  # Vegetative
        elif self.day <= 20:
            self.stage = 1  # Flowering
        else:
            self.stage = 2  # Maturation

        # State Reward Calculation
        if self.moisture == 1:  # Optimal moisture
            reward += 10.0
            self.crop_health = min(100.0, self.crop_health + 1.5)
            if self.stage == 1:  # Extra critical reward for flowering stage
                reward += 5.0
        elif self.moisture == 0:  # Dry/Low
            reward -= 6.0
            self.crop_health = max(0.0, self.crop_health - 3.0)
        elif self.moisture == 2:  # Waterlogged
            reward -= 8.0
            self.crop_health = max(0.0, self.crop_health - 2.5)

        # Over-watering penalty when already waterlogged
        if action in [2, 3] and self.moisture == 2:
            reward -= 12.0

        done = self.day >= self.max_days or self.crop_health <= 0

        info = {
            "day": self.day,
            "crop_health": self.crop_health,
            "moisture_desc": MOISTURE_LEVELS[self.moisture],
            "weather_desc": WEATHER_CONDITIONS[self.weather],
            "stage_desc": CROP_STAGES[self.stage]
        }

        next_state = encode_state(self.moisture, self.weather, self.stage)
        return next_state, reward, done, info


class QLearningAgent:
    """
    Tabular Q-Learning Agent implementing Bellman Optimality updates:
    Q(s,a) <- Q(s,a) + alpha * [r + gamma * max_a' Q(s', a') - Q(s,a)]
    """

    def __init__(self, num_states: int = NUM_STATES, num_actions: int = NUM_ACTIONS,
                 alpha: float = 0.1, gamma: float = 0.95, epsilon: float = 1.0,
                 epsilon_decay: float = 0.995, min_epsilon: float = 0.01):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha            # Learning rate
        self.gamma = gamma            # Discount factor
        self.epsilon = epsilon        # Exploration rate
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

        # Initialize Q-table with zeros
        self.q_table = np.zeros((num_states, num_actions))

    def choose_action(self, state: int, evaluate: bool = False) -> int:
        """Select action using Epsilon-Greedy strategy (or purely greedy if evaluate=True)."""
        if not evaluate and random.random() < self.epsilon:
            return random.randint(0, self.num_actions - 1)
        return int(np.argmax(self.q_table[state]))

    def update(self, state: int, action: int, reward: float, next_state: int, done: bool):
        """Perform Bellman Optimality update step on Q-table."""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward if done else reward + self.gamma * self.q_table[next_state, best_next_action]
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.alpha * td_error

    def decay_epsilon(self):
        """Decay exploration rate after each episode."""
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)


def train_q_learning(episodes: int = 1000) -> tuple[QLearningAgent, list[float]]:
    """Train the Q-Learning agent on the CropIrrigationEnv across specified episodes."""
    env = CropIrrigationEnv()
    agent = QLearningAgent()
    episode_rewards = []

    print(f"[TRAIN] Training Q-Learning Agent for {episodes} episodes...")
    for ep in range(1, episodes + 1):
        state = env.reset()
        total_reward = 0.0
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.update(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

        agent.decay_epsilon()
        episode_rewards.append(total_reward)

        if ep % 200 == 0 or ep == episodes:
            avg_reward = np.mean(episode_rewards[-50:])
            print(f"   Episode {ep}/{episodes} | Avg Reward (last 50): {avg_reward:.2f} | Epsilon: {agent.epsilon:.4f}")

    print("[SUCCESS] Training Complete!\n")
    return agent, episode_rewards


def evaluate_policy(agent: QLearningAgent, days: int = 30) -> pd.DataFrame:
    """Run a deterministic evaluation simulation using the learned policy."""
    env = CropIrrigationEnv(seed=100)
    state = env.reset()
    history = []

    for day in range(1, days + 1):
        action = agent.choose_action(state, evaluate=True)
        m, w, s = decode_state(state)
        next_state, reward, done, info = env.step(action)

        history.append({
            "Day": day,
            "Crop Stage": CROP_STAGES[s],
            "Weather": WEATHER_CONDITIONS[w],
            "Soil Moisture": MOISTURE_LEVELS[m],
            "Action Chosen": ACTIONS[action],
            "Reward": round(reward, 2),
            "Crop Health Score": round(info["crop_health"], 1)
        })

        state = next_state
        if done:
            break

    return pd.DataFrame(history)


def plot_results(episode_rewards: list[float], q_table: np.ndarray, output_path: str = "q_learning_results.png"):
    """Generate and save comprehensive visualizations for Q-Learning convergence & policy."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Learning Curve
    smoothed = pd.Series(episode_rewards).rolling(window=30, min_periods=1).mean()
    axes[0].plot(episode_rewards, alpha=0.3, color="teal", label="Raw Episode Reward")
    axes[0].plot(smoothed, color="darkgreen", linewidth=2, label="30-Episode Moving Avg")
    axes[0].set_title("1. Q-Learning Reward Convergence", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Episode")
    axes[0].set_ylabel("Total Episode Reward")
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend()

    # 2. Q-Table Heatmap (First 15 States)
    im = axes[1].imshow(q_table[:15, :], cmap="YlGnBu", aspect="auto")
    axes[1].set_title("2. Learned Q-Table Heatmap (States 0-14)", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Actions (0: None, 1: Light, 2: Heavy, 3: Fert)")
    axes[1].set_ylabel("State ID")
    axes[1].set_xticks(range(4))
    fig.colorbar(im, ax=axes[1], label="Q-Value")

    # 3. Action Preference by Moisture Level
    moisture_action_counts = np.zeros((3, 4))
    for s_id in range(NUM_STATES):
        m, _, _ = decode_state(s_id)
        best_act = np.argmax(q_table[s_id])
        moisture_action_counts[m, best_act] += 1

    actions_short = ["Do Nothing", "Light Irr", "Heavy Irr", "Fertilizer"]
    x = np.arange(3)
    width = 0.2
    for a in range(4):
        axes[2].bar(x + a * width, moisture_action_counts[:, a], width, label=actions_short[a])

    axes[2].set_title("3. Optimal Action Distribution by Soil Moisture", fontsize=12, fontweight="bold")
    axes[2].set_xticks(x + 1.5 * width)
    axes[2].set_xticklabels(MOISTURE_LEVELS)
    axes[2].set_ylabel("State Count")
    axes[2].legend()
    axes[2].grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[PLOT] Visualization saved to: {output_path}")


def main():
    print("=========================================================================")
    print("  Practical 11: Reinforcement Learning (Q-Learning Irrigation Agent)")
    print("=========================================================================\n")

    # 1. Train Agent
    agent, rewards = train_q_learning(episodes=1000)

    # 2. Evaluate Policy
    df_eval = evaluate_policy(agent, days=30)
    print("[EVAL] 30-Day Policy Execution Sample:")
    print(df_eval.head(10).to_string(index=False))
    print("\n...")

    # 3. Save Model Artifacts
    output_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(output_dir, "q_learning_results.png")
    plot_results(rewards, agent.q_table, output_path=img_path)

    # Save trained model to Backend saved_models directory if available
    backend_model_dir = os.path.join(output_dir, "..", "Backend", "ai", "saved_models")
    os.makedirs(backend_model_dir, exist_ok=True)
    model_save_path = os.path.join(backend_model_dir, "q_learning_irrigation.joblib")
    joblib.dump({"q_table": agent.q_table, "states": NUM_STATES, "actions": NUM_ACTIONS}, model_save_path)
    print(f"[SAVE] Trained Q-Table saved to: {model_save_path}")

    print("\n[SUCCESS] Practical 11 Reinforcement Learning Execution Completed Successfully!")


if __name__ == "__main__":
    main()
