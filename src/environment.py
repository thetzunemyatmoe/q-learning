import numpy as np
import random
import matplotlib.pyplot as plt


class GridEnvironment:
    def __init__(self, size):
        self.size = size

        # 2D array of all zeros
        self.the_grid = np.zeros([size, size], dtype=int)

        # self.start. self.goal ---> (x, y)
        self.start, self.goal = self._initialize_positions()

        # Function to add obstacles in the grid
        self._add_obstacles()

        # Rover's position = Start position ---> (x, y)
        self.rover = self.start

        # Is goal reached?
        self.isReached = False

        self.initialized = False  # Flag to track if the grid has been initialized

        # Initialize the plot for dynamic updates
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots()  # Create a figure and axis for visualization

    # Setting  random start and goal position as (x, y)
    def _initialize_positions(self):
        # Starting position / (x, y)
        start = (random.randint(0, 3), random.randint(0, 3))

        # Goal position / (x, y)
        goal = (random.randint(self.size - 4, self.size - 1),
                random.randint(self.size - 4, self.size - 1))

        # No clash between start and goal postion
        while start == goal:
            goal = (random.randint(self.size - 4, self.size - 1),
                    random.randint(self.size - 4, self.size - 1))

        # Mark the start and goal on the grid
        # self.the_grid[(x,y)] = value
        self.the_grid[start] = 1
        self.the_grid[goal] = 2

        # (x, y)
        return start, goal

    def _add_obstacles(self):

        # Number of obstacles (25% of the grid)
        num_obstacles = int(self.size * self.size * 0.25)

        # List of all possible positions on the grid (x,y)
        available_positions = [(i, j) for i in range(self.size) for j in range(
            self.size) if (i, j) != self.start and (i, j) != self.goal]

        # Randomly select positions for set number of obstacles --> (x, y)
        obstacle_positions = random.sample(available_positions, num_obstacles)

        # Set obstacles value to -1 on the grid
        for pos in obstacle_positions:
            self.the_grid[pos] = -1

    # Rover action
    # 1. Calculate the new coordinates based on the action
    # 2. Get the reward for moving to the new coordinate from reward function
    # 3. If the new coordinate is valid (Move into an empty cell, Move into the goal cell, Move to visited cell)
        # a. Update the actual coordinate (x, y) of rover
        # b. Leave the trace in the grid
        # c. Mark the new coordiate in the grid with appropriate indicator
    # Return the calculated reward
    # direction from ['up', 'down', 'left', 'right]
    def move_rover(self, direction):
        # print(self.the_grid)

        # Gettting current rover position
        curr_x, curr_y = self.rover

        if direction == 'up':
            new_position = (curr_x - 1, curr_y)
        elif direction == "down":
            new_position = (curr_x + 1, curr_y)
        elif direction == "left":
            new_position = (curr_x, curr_y - 1)
        elif direction == "right":
            new_position = (curr_x, curr_y + 1)

        # print(
        #     f'Old position ({curr_x}, {curr_y}) --> New position {new_position}')

        reward = self.get_reward(new_position=new_position)

        # Goal state is reached
        if reward == 100:
            self.the_grid[self.rover] = 3  # Leave a trace
            self.rover = new_position  # Update rover's new position
            # Mark rover's new position in the grid (Goal)
            self.the_grid[self.rover] = 9
            self.isReached = True
        # Moving in previously visited cell or Moving in new cell
        elif reward == -2 or reward == 5:
            self.the_grid[self.rover] = 3  # Leave a trace
            self.rover = new_position  # Update rover's new position
            self.the_grid[self.rover] = 1  # Mark rover position in the grid

        self.visualize_grid()
        return reward

    # def move_rover(self, direction):
    #     # Current rover position (x, y)
    #     x, y = self.rover
    #     print('Current x: ', x)
    #     print('Current y: ', y)
    #     print('Action take: ', direction)

    #     # Map direction to coordinates change
    #     if direction == "up":
    #         possible_new_position = (x - 1, y)
    #     elif direction == "down":
    #         possible_new_position = (x + 1, y)
    #     elif direction == "left":
    #         possible_new_position = (x, y - 1)
    #     elif direction == "right":
    #         possible_new_position = (x, y + 1)

    #     reward = self.get_reward(new_position=possible_new_position)

    #     # Reward -> 50 -> Goal is reached
    #     if reward == 50:
    #         self.the_grid[self.rover] = 3  # Leave a trace
    #         self.rover = possible_new_position
    #         self.the_grid[self.rover] = 69  # Mark that the goal is reached
    #     # Reward -> -1 -> Possible path
    #     elif reward == -1:
    #         self.the_grid[self.rover] = 3  # Leave a trace
    #         self.rover = possible_new_position
    #         self.the_grid[self.rover] = 1  # Mark that the goal is reached
        # return reward

        # # New_position - (x, y)
        # # Check if the new position is within bounds and not an obstacle - Move the robot to new position and Leave a trace
        # if (0 <= possible_new_position[0] < self.size) and (0 <= possible_new_position[1] < self.size) and self.the_grid[possible_new_position] != -1:
        #     # Mark the old rover position with 3 (trace), if it's not the goal
        #     if self.the_grid[possible_new_position] != 2:  # Avoid overwriting the goal
        #         # Mark previous position with trace
        #         self.the_grid[self.rover] = 3

        #     if self.the_grid[new_position] == 2:
        #         self.the_grid[new_position] = 69
        #         print("the agent has reached the goal ")
        #     # Move the rover to the new position (mark it with 1 for rover)
        #     self.rover = new_position
        #     self.the_grid[self.rover] = 1  # Set new rover position to 1 (blue)
        # else:
        #     print(
        #         f"Invalid move to {new_position}. Either out of bounds or an obstacle.")
        #     return -100, self.get_state_index()

        # Visualize the grid after the move
        # self.visualize_grid()

        # return self.get_reward(), self.get_state_index()

    # Reward function

    def get_reward(self, new_position):
        # Penalize for moving out of bound
        if (new_position[0] < 0 or new_position[0] >= self.size) or (new_position[1] < 0 or new_position[1] >= self.size):
            return -20
        # Reward for reaching the goal
        elif self.the_grid[new_position] == 2:
            print("goal is reached")
            return 100
        # Reward for exploring new cell
        elif self.the_grid[new_position] == 0:
            return 5
        # Penlaize for revisiting previously visited cells
        elif self.the_grid[new_position] == 3:
            return -2
        # Penalize for hiiting the obstalce
        elif self.the_grid[new_position] == -1:
            return -50

    def visualize_grid(self):
        # Map the grid values to colors
        cmap = {
            0: [1, 1, 1],  # Empty space (white)
            -1: [0, 0, 0],  # Obstacle (black)
            3: [1, 0, 0],  # Trace (red)
            1: [0, 0, 1],  # Rover (blue)
            2: [0, 1, 0],  # Goal (green)
            9: [1, 1, 0],  # Yellow

        }

        # Create a color grid where each cell is mapped to the appropriate color
        color_grid = np.zeros((self.size, self.size, 3))

        for i in range(self.size):
            for j in range(self.size):
                # Default gray for unknown values
                color_grid[i, j] = cmap.get(
                    self.the_grid[i, j], [0.5, 0.5, 0.5])

        # Clear the current figure
        self.ax.cla()  # Clear axis
        self.ax.imshow(color_grid)  # Redraw grid
        self.ax.axis('off')  # Hide axis
        plt.draw()  # Redraw the plot
        plt.pause(0.00001)  # Pause to allow visualization to update

    def get_state_index(self):
        # Convert the 2D position of the rover into a 1D state index
        return self.rover[0] * self.size + self.rover[1]

    def is_terminal_state(self):
        return self.rover == self.goal or self.the_grid[self.rover] == -1

    def reset(self):
        # Initialize grid, start, and goal only once
        if not self.initialized:
            self.the_grid = np.zeros([self.size, self.size], dtype=int)
            self.start, self.goal = self._initialize_positions()
            self.rover = self.start
            self.the_grid[self.start] = 1
            self.the_grid[self.goal] = 2
            self._add_obstacles()
            self.initialized = True
        else:
            # Reset rover to start position and clear any traces
            self.the_grid = np.where(self.the_grid == 3, 0, self.the_grid)
            self.the_grid[self.rover] = 0  # Clear previous rover position
            self.rover = self.start
            self.the_grid[self.rover] = 1
            self.the_grid[self.goal] = 2

        self.isReached = False  # Reset goal status

    def get_grid(self):
        return self.the_grid

    def get_start(self):
        return self.start

    def get_goal(self):
        return self.goal

    def get_rover_position(self):
        return self.rover
