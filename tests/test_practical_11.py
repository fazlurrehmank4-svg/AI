"""
Unit Tests for Practical 11: Reinforcement Learning (Q-Learning Agent & Environment)
"""

import os
import sys
import numpy as np
import pytest

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Practical_11_Reinforcement_Learning.rl_irrigation_agent import (
    CropIrrigationEnv, QLearningAgent, encode_state, decode_state, train_q_learning
)
from Backend.ai.rl_irrigation_agent import RLIrrigationAgent


def test_state_encoding_decoding():
    """Verify state index encoding and decoding bijectivity."""
    for m in range(3):
        for w in range(3):
            for s in range(3):
                encoded = encode_state(m, w, s)
                m_dec, w_dec, s_dec = decode_state(encoded)
                assert (m, w, s) == (m_dec, w_dec, s_dec), f"Mismatch for state ({m}, {w}, {s})"


def test_environment_reset_and_step():
    """Verify environment initialization and transition step mechanics."""
    env = CropIrrigationEnv(seed=42)
    state = env.reset()
    assert 0 <= state < 27
    assert env.day == 1

    next_state, reward, done, info = env.step(action=1)  # Light irrigation
    assert 0 <= next_state < 27
    assert isinstance(reward, float)
    assert isinstance(done, bool)
    assert "crop_health" in info
    assert env.day == 2


def test_q_learning_update():
    """Test Bellman optimality update step on Q-table."""
    agent = QLearningAgent(alpha=0.5, gamma=0.9)
    state = 0
    action = 1
    reward = 10.0
    next_state = 1

    # Initial Q-value should be 0.0
    assert agent.q_table[state, action] == 0.0

    agent.update(state, action, reward, next_state, done=False)
    # Target = 10.0 + 0.9 * 0.0 = 10.0; Updated Q = 0 + 0.5*(10.0 - 0) = 5.0
    assert agent.q_table[state, action] == 5.0


def test_training_convergence():
    """Verify Q-learning agent trains cleanly and improves rewards."""
    agent, rewards = train_q_learning(episodes=100)
    assert len(rewards) == 100
    assert agent.q_table.shape == (27, 4)
    # Verify non-zero values learned in Q-table
    assert np.any(agent.q_table != 0.0)


def test_backend_rl_agent_recommendation():
    """Verify Backend RL agent generates valid action recommendations."""
    service = RLIrrigationAgent()
    res = service.recommend_action(soil_moisture_status="low", weather_status="sunny", crop_stage="flowering")
    assert "action" in res
    assert "action_id" in res
    assert "confidence" in res
    assert res["action_id"] in [0, 1, 2, 3]
