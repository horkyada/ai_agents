"""
Evaluate trained Q-learning agent on MountainCar
"""
import time
from mountain_car import MountainCarEnv, QLearningAgent


def evaluate(model_path="models/q_table_trained.pkl", n_episodes=5):
    """Run the trained agent with visualization"""

    # Create environment with rendering
    env = MountainCarEnv(render_mode="human")

    # Create and load agent
    agent = QLearningAgent()
    agent.load(model_path)

    print("Evaluating trained Q-learning agent")
    print("=" * 60)
    print(f"Model: {model_path}")
    print(f"Epsilon (exploration rate): {agent.epsilon:.3f}")
    print("=" * 60)

    successes = 0
    total_steps = []

    for episode in range(n_episodes):
        state, _ = env.reset()
        total_reward = 0
        steps = 0
        done = False
        max_position = state[0]

        print(f"\nEpisode {episode + 1}/{n_episodes}")
        print(f"Initial position: {state[0]:.3f}, velocity: {state[1]:.3f}")

        while not done:
            # Use trained policy (no exploration)
            action = agent.get_action(state, training=False)

            # Take step
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            max_position = max(max_position, next_state[0])

            state = next_state
            total_reward += reward
            steps += 1

            # Print progress every 20 steps
            if steps % 20 == 0:
                position, velocity = state
                print(f"  Step {steps}: pos={position:.3f}, vel={velocity:.3f}")

            # Slow down for visualization
            time.sleep(0.02)

        total_steps.append(steps)

        # Check if goal reached
        if max_position >= 0.5:
            successes += 1
            print(f"✓ SUCCESS! Reached goal in {steps} steps")
        else:
            print(f"✗ Failed. Max position: {max_position:.3f}, Steps: {steps}")

        print(f"Total reward: {total_reward:.1f}")

    env.close()

    print("\n" + "=" * 60)
    print("Evaluation Summary")
    print("=" * 60)
    print(f"Success rate: {successes}/{n_episodes} ({successes/n_episodes*100:.1f}%)")
    print(f"Average steps: {sum(total_steps)/len(total_steps):.1f}")
    if successes > 0:
        successful_steps = [s for i, s in enumerate(total_steps) if total_steps[i] < 200]
        print(f"Average steps (successful): {sum(successful_steps)/len(successful_steps):.1f}")


if __name__ == "__main__":
    evaluate()
