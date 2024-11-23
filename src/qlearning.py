import numpy as np
import random
from environment import GridEnvironment
import time


class QLearning:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):
        self.env = GridEnvironment(10)
        # Q-Table for all states and actions
        self.q_table = np.zeros((self.env.size * self.env.size, 4))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        self.actions = ['up', 'down', 'left', 'right']  # Possible actions

    def choose_action(self):
        return random.choice(self.actions)

    def learn(self, episodes):

        for episode in range(episodes):
            print(f'Environemnt setting up for episode {episode}')
            time.sleep(3)
            self.env.reset()

            while not q_learning.env.isReached:
                reward = q_learning.env.move_rover(q_learning.choose_action())


q_learning = QLearning()
q_learning.learn(10)
