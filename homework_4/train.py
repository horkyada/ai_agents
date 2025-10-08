"""
Train Q-learning agent on MountainCar
"""
import numpy as np
from mountain_car import MountainCarEnv, QLearningAgent


def train(n_episodes=5000, save_freq=1000):
    """Train the Q-learning agent"""

    # Create environment (no rendering during training for speed)
    env = MountainCarEnv(render_mode=None)

    # Create agent
    agent = QLearningAgent(
        n_actions=3,
        learning_rate=0.1,
        discount_factor=0.99,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.01,
        n_bins=(20, 20),
    )

    # Training metrics
    episode_rewards = []
    episode_lengths = []
    max_positions = []
    success_count = 0

    print("Starting Q-learning training...")
    print(f"Episodes: {n_episodes}")
    print(f"State bins: {agent.n_bins}")
    print(f"Goal position: 0.5 (flag at the top)")
    print("=" * 60)

    for episode in range(n_episodes):
        state, _ = env.reset()
        total_reward = 0
        steps = 0
        done = False
        max_position = state[0]  # Track furthest position reached

        while not done:
            # Select action
            action = agent.get_action(state, training=True)

            # Take step
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            # Track max position reached
            max_position = max(max_position, next_state[0])

            # Update agent
            agent.update(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward
            steps += 1

        # Track metrics
        episode_rewards.append(total_reward)
        episode_lengths.append(steps)
        max_positions.append(max_position)

        # Check if solved (reached goal)
        if steps < 200:  # Goal reached before max steps
            success_count += 1

        # Decay exploration
        agent.decay_epsilon()

        # Print progress
        if (episode + 1) % 100 == 0:
            avg_reward = np.mean(episode_rewards[-100:])
            avg_length = np.mean(episode_lengths[-100:])
            avg_max_pos = np.mean(max_positions[-100:])
            best_pos_recent = max(max_positions[-100:])
            success_rate = success_count / 100

            print(f"Episode {episode + 1}/{n_episodes}")
            print(f"  Avg Reward: {avg_reward:.1f}")
            print(f"  Avg Steps: {avg_length:.1f}")
            print(f"  Avg Max Position: {avg_max_pos:.3f} (goal: 0.5)")
            print(f"  Best Position: {best_pos_recent:.3f}")
            print(f"  Success Rate: {success_rate:.1%}")
            print(f"  Epsilon: {agent.epsilon:.3f}")
            print()

            success_count = 0

        # Save checkpoint
        if (episode + 1) % save_freq == 0:
            import os
            os.makedirs("models", exist_ok=True)
            agent.save(f"models/q_table_ep{episode + 1}.pkl")

    env.close()

    # Save final model
    import os
    os.makedirs("models", exist_ok=True)
    agent.save("models/q_table_trained.pkl")

    # Save training metrics
    np.savez(
        "training_metrics.npz",
        rewards=episode_rewards,
        lengths=episode_lengths,
        max_positions=max_positions,
    )

    print("=" * 60)
    print("Training complete!")
    print(f"Final epsilon: {agent.epsilon:.3f}")
    print(f"Final 100 episodes avg reward: {np.mean(episode_rewards[-100:]):.1f}")
    print(f"Final 100 episodes avg steps: {np.mean(episode_lengths[-100:]):.1f}")


if __name__ == "__main__":
    train()
