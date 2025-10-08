"""
MountainCar environment wrapper
"""
import gymnasium as gym


class MountainCarEnv:
    """Wrapper for the MountainCar-v0 environment"""

    def __init__(self, render_mode="human"):
        self.env = gym.make("MountainCar-v0", render_mode=render_mode)
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def reset(self):
        """Reset the environment"""
        observation, info = self.env.reset()
        return observation, info

    def step(self, action):
        """Take a step in the environment"""
        return self.env.step(action)

    def close(self):
        """Close the environment"""
        self.env.close()

    def get_state_info(self, observation):
        """Get human-readable state information"""
        position, velocity = observation
        return {
            "position": position,
            "velocity": velocity,
            "distance_to_goal": 0.5 - position,  # Goal is at position 0.5
        }