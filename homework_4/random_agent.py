"""
Random agent demo - shows how a random agent performs (poorly!)
"""
import time
from mountain_car import MountainCarEnv


def random_agent(n_episodes=3):
    """Run random agent for comparison"""

    env = MountainCarEnv(render_mode="human")

    print("Random Agent Demo")
    print("=" * 60)
    print("This shows how a random agent performs.")
    print("It will likely fail to reach the goal!")
    print("=" * 60)

    for episode in range(n_episodes):
        observation, info = env.reset()
        total_reward = 0
        steps = 0
        max_position = observation[0]

        print(f"\nEpisode {episode + 1}/{n_episodes} started")
        print(f"Initial position: {observation[0]:.3f}, velocity: {observation[1]:.3f}")

        done = False
        while not done:
            # Random action
            action = env.action_space.sample()

            observation, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            max_position = max(max_position, observation[0])

            done = terminated or truncated
            time.sleep(0.01)

        if max_position >= 0.5:
            print(f"✓ SUCCESS! (Lucky!) Reached goal in {steps} steps")
        else:
            print(f"✗ Failed. Max position: {max_position:.3f}, Steps: {steps}")
        print(f"Total reward: {total_reward:.1f}")

    env.close()


if __name__ == "__main__":
    random_agent()
