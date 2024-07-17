from maze import Maze

class Level:
    def __init__(self, size):
        self.current_level = 1
        self.size = size
        self.wall_thickness = 1  # Initial wall thickness
        self.wall_thickness_decrease_rate = 0.9  # Control wall thinning rate
        self.maze = Maze(self.size, self.wall_thickness)

    def get_maze(self):
        return self.maze.generate_maze()

    def next_level(self):
        self.current_level += 1
        self.size = min(self.size + 2, 31)  # Increment size for next level, max 31
        self.wall_thickness = max(0.2, self.wall_thickness * self.wall_thickness_decrease_rate)
        self.maze = Maze(self.size, self.wall_thickness)
        return self.get_maze()

    def get_current_level(self):
        return self.current_level

    def get_wall_thickness(self):
        return self.wall_thickness

    def get_maze_size(self):
        return self.size