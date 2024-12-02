import numpy as np
import random
import matplotlib.pyplot as plt


class GridEnvironment:
    def __init__(self, size):
        self.size = size
        # Initialize the original grid configuration
        self.original_grid = np.zeros([size, size], dtype=int)

        # 2D array of all zeros
        self.the_grid = np.zeros([size, size], dtype=int)

        # State coordinates (x, y)
        self.start = (1, 0)
        self.original_grid[self.start] = 1
        # Goal coordinates (x, y)
        self.goal = self._initialize_goal()
        self.original_grid[self.goal] = 2

        # Function to add obstacles in the grid
        self.obstacle_indexes_array = self._add_obstacles()

        # Rover's position = Start position ---> (x, y)
        self.rover = self.start
        # The grid to train on
        self.the_grid = self.original_grid.copy()

        # Is goal reached?
        self.isReached = False
        # Initialize the plot for dynamic updates
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots()  # Create a figure and axis for visualization

    # Setting  random goal position as (x, y)

    def _initialize_goal(self):
        # Goal position
        goal = (random.randint(self.size - 4, self.size - 1),
                random.randint(self.size - 4, self.size - 1))
        # (x, y)
        return goal

    def _add_obstacles(self):
        arr = []

        # Number of obstacles (25% of the grid)
        num_obstacles = int(self.size * self.size * 0.25)
        # print(f'Number of obstacles on the grid --> {num_obstacles}\n')

        # List of all possible positions on the grid (x,y)
        available_positions = [(i, j) for i in range(self.size) for j in range(
            self.size) if (i, j) != self.start and (i, j) != self.goal]
        # print(f'Available positions on the grid \n {available_positions}\n')

        # Randomly select positions for set number of obstacles --> (x, y)
        obstacle_positions = random.sample(available_positions, num_obstacles)
        # print(f'Obstacle positions on the grid \n{obstacle_positions}\n')

        # Mark obstacles as -1 on the grid
        for pos in obstacle_positions:
            arr.append((pos[0] * self.size) + pos[1])
            self.original_grid[pos] = -1
        arr.sort()

        return arr

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
        # self.visualize_grid()
        return reward

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
            # print(f'new_position is the obstacle')
            return -100000

        return 0

    def goal_state_index(self):
        return (self.goal[0] * self.size) + self.goal[1]

    def get_current_state_index(self):
        # Convert the 2D position of the rover into a 1D state index
        return (self.rover[0] * self.size) + self.rover[1]

    def reset(self):
        # Rover's position = Start position ---> (x, y)
        self.rover = self.start
        self.the_grid = self.original_grid.copy()
        self.isReached = False

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
