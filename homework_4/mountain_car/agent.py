"""
Q-learning agent for MountainCar
"""
import numpy as np
import pickle


class QLearningAgent:
    """Q-learning agent with discrete state space"""

    def __init__(
        self,
        n_actions=3,
        learning_rate=0.1,
        discount_factor=0.99,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.01,
        n_bins=(20, 20),  # Bins for [position, velocity]
    ):
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.n_bins = n_bins

        # Q-table: shape (position_bins, velocity_bins, n_actions)
        self.q_table = np.zeros((*n_bins, n_actions))

        # State space bounds for MountainCar
        self.state_bounds = [
            (-1.2, 0.6),  # position
            (-0.07, 0.07),  # velocity
        ]

    def discretize_state(self, state):
        """Convert continuous state to discrete bin indices"""
        position, velocity = state
        bounds = self.state_bounds

        # Discretize each dimension
        position_bin = int(
            np.clip(
                (position - bounds[0][0]) / (bounds[0][1] - bounds[0][0]) * self.n_bins[0],
                0,
                self.n_bins[0] - 1,
            )
        )
        velocity_bin = int(
            np.clip(
                (velocity - bounds[1][0]) / (bounds[1][1] - bounds[1][0]) * self.n_bins[1],
                0,
                self.n_bins[1] - 1,
            )
        )

        return (position_bin, velocity_bin)

    def get_action(self, state, training=True):
        """Select action using epsilon-greedy policy"""
        if training and np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)

        # Exploit: choose best action
        discrete_state = self.discretize_state(state)
        return np.argmax(self.q_table[discrete_state])

    def update(self, state, action, reward, next_state, done):
        """Update Q-table using Q-learning update rule"""
        discrete_state = self.discretize_state(state)
        discrete_next_state = self.discretize_state(next_state)

        # Current Q-value
        current_q = self.q_table[discrete_state][action]

        # Target Q-value
        if done:
            target_q = reward
        else:
            target_q = reward + self.gamma * np.max(self.q_table[discrete_next_state])

        # Q-learning update
        self.q_table[discrete_state][action] += self.lr * (target_q - current_q)

    def decay_epsilon(self):
        """Decay exploration rate"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save(self, filepath):
        """Save Q-table and parameters"""
        data = {
            "q_table": self.q_table,
            "epsilon": self.epsilon,
            "n_bins": self.n_bins,
            "state_bounds": self.state_bounds,
        }
        with open(filepath, "wb") as f:
            pickle.dump(data, f)
        print(f"Agent saved to {filepath}")

    def load(self, filepath):
        """Load Q-table and parameters"""
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        self.q_table = data["q_table"]
        self.epsilon = data["epsilon"]
        self.n_bins = data["n_bins"]
        self.state_bounds = data["state_bounds"]
        print(f"Agent loaded from {filepath}")