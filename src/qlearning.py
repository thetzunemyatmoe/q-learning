import numpy as np
import random
from environment import GridEnvironment
import time
import os


class QLearning:
    def __init__(self, epsilon_decay=0.99, min_epsilon=0.1):
        self.env = GridEnvironment(20)
        # Q-Table for all states and actions
        self.q_table = np.zeros((self.env.size * self.env.size, 4))

        # Hyperparameters
        self.learning_rate = 0
        self.discount_factor = 0
        self.epsilon = 0
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

        # Possible action in each state
        self.actions = ['up', 'down', 'left', 'right']

    def choose_action(self, current_state):
        # Explore with probability epsilon
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)  # Random action
        # Exploit with probability 1 - epsilon (choose action with highest Q-value
        return self.actions[np.argmax(self.q_table[current_state, :])]

    def bellham(self, current_state, new_state, action, reward):
        print(self.discount_factor)
        print(self.learning_rate)

        # Get the Q-value for the current state-action pair
        q_value = self.q_table[current_state, action]

        # Calculate the maximum expected Q-value for the next state
        max_next_q_value = np.max(self.q_table[new_state, :])

        # Update the Q-table using the Bellman equation
        new_q_value = q_value + self.learning_rate * \
            (reward + self.discount_factor * max_next_q_value - q_value)
        self.q_table[current_state, action] = new_q_value

    def learn(self, episodes, learning_rate, discount_factor, epsilon):
        print("Learning has started")
        self.q_table = np.zeros((self.env.size * self.env.size, 4))

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        print(
            f'Leanring rate [{self.learning_rate}] | Discount_factor [{self.discount_factor}] | Epsilon [{self.epsilon}]')
        steps_per_episode = []
        for episode in range(episodes):
            steps = 0
            total_reward = 0
            # Resetting the environment
            self.env.reset()
            print(
                f'For episode{episode} : Leanring rate [{self.learning_rate}] | Discount_factor [{self.discount_factor}] | Epsilon [{self.epsilon}]')

            while not self.env.isReached:
                current_state = self.env.get_current_state_index()
                action = self.choose_action(current_state=current_state)
                reward = self.env.move_rover(action)
                new_state = self.env.get_current_state_index()
                # print(
                #     f'Current state [{current_state}] + Action [{action}] ---> New State[{new_state}]')

                self.bellham(current_state, new_state,
                             self.actions.index(action), reward)
                total_reward += reward
                steps += 1

                # Visualize the grid at each step
            steps_per_episode.append(steps)
            # print(
            #     f'Episode {episode+1}: Total Reward: {total_reward}, Steps: {steps}')
            # Epsilon decay for exploration vs exploitation
            self.epsilon = max(
                self.min_epsilon, self.epsilon * self.epsilon_decay)

         # Optionally, visualize the results or save them
        # print('Training completed. Total steps per episode: ', steps_per_episode)
        # print('---------------------------------------------------')
        print(self.q_table)
        time.sleep(5)

    def save_data(self):
        q_table = self.q_table
        obstacles = self.env.obstacle_indexes_array    # Example obstacle indices
        goal_state = self.env.goal_state_index()

        np.savez('q_learning_data.npz', q_table=q_table,
                 obstacles=obstacles, goal_position=goal_state)
        # Specify directory and filename
        directory = '/Users/thetzunemyatmoe/Documents'
        filename = 'q_learning_data.npz'
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Save file
        file_path = os.path.join(directory, filename)
        np.savez(file_path, q_table=q_table, obstacles=obstacles,
                 goal_state=goal_state)
        print(f"Data saved successfully at {file_path}")


# q_learning = QLearning()
# q_learning.learn(1500, 0.3, 0.95, 0.8)
# q_learning.save_data()
# q_learning.learn(1500, 0.9, 0.95, 0.8)
# q_learning.save_data()
