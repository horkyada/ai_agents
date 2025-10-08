"""
Demo: Watch trained Q-learning agent on MountainCar
This uses the pre-trained model included in the repository.
"""
from evaluate import evaluate

if __name__ == "__main__":
    print("=" * 60)
    print("MountainCar Q-Learning Demo")
    print("=" * 60)
    print("This demo uses a pre-trained Q-learning agent.")
    print("Watch how it builds momentum by going back and forth!")
    print("=" * 60)
    print()

    evaluate(model_path="models/q_table_demo.pkl")
