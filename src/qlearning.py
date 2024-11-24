import numpy as np
import random
from environment import GridEnvironment
import time


class QLearning:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.env = GridEnvironment(20)
        # Q-Table for all states and actions
        self.q_table = np.zeros((self.env.size * self.env.size, 4))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.actions = ['up', 'down', 'left', 'right']  # Possible actions

        print(self.q_table.shape)

    def choose_action(self, current_state):
        # return random.choice(self.actions)
        # Explore with probability epsilon
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)  # Random action

        # Exploit with probability 1 - epsilon (choose action with highest Q-value)
        # Index of the highest value
        actions = np.argmax(self.q_table[current_state, :])

        return self.actions[np.random.choice([actions])]

    def bellham(self, current_state, new_state, action, reward):
        # print(f'Current state {current_state}')
        # print(f'Action {action}')
        # print(f'New State {new_state}')
        # print(f'Reward {reward}\n------------------')
        # Get the Q-value for the current state-action pair
        q_value = self.q_table[current_state, action]

        # Calculate the maximum expected Q-value for the next state
        max_next_q_value = np.max(self.q_table[new_state, :])

        # Update the Q-table using the Bellman equation
        new_q_value = q_value + self.learning_rate * \
            (reward + self.discount_factor * max_next_q_value - q_value)
        self.q_table[current_state, action] = new_q_value

    def learn(self, episodes):

        for episode in range(episodes):
            print(self.q_table)
            # Resetting the environment
            print(f'Environemnt setting up for episode {episode}')
            time.sleep(3)
            self.env.reset()

            while not q_learning.env.isReached:
                # Current state of the rover (Scalar value acted as an index to access the Q table assiociated with the current state)
                current_state = self.env.get_state_index()

                # Choose the action
                action = self.choose_action(current_state=current_state)
                # Retrieve the reward, update the grid according and visualize
                reward = q_learning.env.move_rover(action)

                # New state of the rover after taking the action (Scalar value acted as an index to access the Q table assiociated with the current state)
                new_state = self.env.get_state_index()

                self.bellham(current_state, new_state,
                             self.actions.index(action), reward)


q_learning = QLearning()
q_learning.learn(100)
