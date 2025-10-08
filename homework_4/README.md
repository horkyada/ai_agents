# MountainCar Q-Learning

Reinforcement Learning implementation for the MountainCar environment using Q-learning with state discretization.

## Assignment

Homework 4 - AI Agents Course

**Task:** Implement a Reinforcement Learning environment and train an agent.

**Solution:** Q-learning agent for OpenAI Gymnasium's MountainCar-v0 environment.

## Environment

**MountainCar-v0:** A car must drive up a steep hill but lacks the power to climb it directly. The agent must learn to build momentum by driving back and forth.

- **State Space:** Position [-1.2, 0.6] and Velocity [-0.07, 0.07]
- **Action Space:** 0 (push left), 1 (do nothing), 2 (push right)
- **Goal:** Reach position 0.5 (flag at the top of the hill)

## Algorithm

**Q-Learning** with discretization:
- State space discretized into 20x20 bins
- Epsilon-greedy exploration (ε starts at 1.0, decays to 0.01)
- Learning rate: 0.1
- Discount factor: 0.99
- Training: 5000 episodes

## Project Structure

```
homework_4/
├── mountain_car/          # Main module
│   ├── __init__.py
│   ├── environment.py     # MountainCar environment wrapper
│   └── agent.py          # Q-learning agent implementation
├── models/               # Trained models
│   └── q_table_demo.pkl  # Pre-trained demo model
├── demo.py              # Quick demo with pre-trained model
├── random_agent.py      # Random baseline comparison
├── train.py             # Training script
├── evaluate.py          # Evaluation script
├── main.py              # Original demo (deprecated, use demo.py)
└── pyproject.toml       # Dependencies
```

## Installation

This project uses `uv` for dependency management:

```bash
cd ai_agents/homework_4
uv sync
```

## Usage

### 1. Demo (Pre-trained Agent)

Watch the pre-trained agent solve the environment:

```bash
uv run demo.py
```

This runs 3 episodes with the included trained model.

### 2. Random Agent (Baseline)

See how a random agent performs (spoiler: poorly):

```bash
uv run random_agent.py
```

### 3. Train Your Own Agent

Train a new Q-learning agent from scratch:

```bash
uv run train.py
```

Training takes ~2-3 minutes for 5000 episodes and shows:
- Progress every 100 episodes
- Average reward, steps, max position reached
- Success rate (% of episodes reaching the goal)
- Current epsilon (exploration rate)

Models are saved to `models/`:
- `models/q_table_ep1000.pkl` - Checkpoint at episode 1000
- `models/q_table_ep2000.pkl` - Checkpoint at episode 2000
- `models/q_table_trained.pkl` - Final trained model

### 4. Evaluate Trained Agent

Test your trained agent with visualization:

```bash
uv run evaluate.py
```

Or evaluate a specific checkpoint:

```bash
uv run python -c "from evaluate import evaluate; evaluate('models/q_table_ep1000.pkl')"
```

## Results

After training for 5000 episodes:
- **Success Rate:** 80-95%
- **Average Steps:** 100-120 (when successful)
- **Convergence:** Agent learns effective momentum-building strategy

The agent learns to:
1. Drive backwards (left) to gain speed
2. Drive forward (right) with momentum
3. Repeat if needed to reach the goal

## Implementation Details

### State Discretization

Continuous state space is discretized into bins:
- Position: 20 bins between -1.2 and 0.6
- Velocity: 20 bins between -0.07 and 0.07
- Total: 20 × 20 = 400 discrete states

### Q-Learning Update

```python
Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
```

Where:
- α = 0.1 (learning rate)
- γ = 0.99 (discount factor)
- r = reward (-1 per step until goal)

### Exploration Strategy

Epsilon-greedy with decay:
- Initial ε = 1.0 (100% random)
- Decay rate = 0.995 per episode
- Minimum ε = 0.01 (1% random)

## Dependencies

- `gymnasium[classic-control]` - RL environment
- `numpy` - Numerical operations
- `pygame` - Visualization

## Files Generated During Training

- `models/q_table_trained.pkl` - Trained Q-table
- `training_metrics.npz` - Rewards, steps, positions per episode
- `models/q_table_ep*.pkl` - Training checkpoints
