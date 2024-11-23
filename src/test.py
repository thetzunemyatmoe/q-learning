from environment import GridEnvironment
import random
# # Example usage
env = GridEnvironment(5)

# Define a list of possible directions
directions = ["up", "down", "left", "right"]

# Simulate 10 random moves
for _ in range(1000):
    random_direction = random.choice(directions)  # Randomly choose a direction
    # Move rover in that direction
    while env.isReached:
        print("hello")
    env.move_rover(random_direction)
    # print(f"\nGrid after moving rover {random_direction}:")
    # print(env.get_grid())
