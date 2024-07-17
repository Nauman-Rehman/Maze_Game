import random

class Maze:
    def __init__(self, size, wall_thickness):
        self.size = size
        self.wall_thickness = wall_thickness

    def generate_maze(self):
        # Initialize maze with walls
        maze = [[1] * self.size for _ in range(self.size)]
        
        def carve_passages_from(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx * 2 , y + dy * 2
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] == 1:
                    maze[ny][nx] = 0
                    maze[y + dy][x + dx] = 0
                    carve_passages_from(nx, ny)
        
        # Start carving from (1, 1)
        maze[1][1] = 0
        carve_passages_from(1, 1)
        
        # Ensure start and end points are accessible
        maze[1][1] = 0
        maze[self.size - 2][self.size - 2] = 0
        
        return maze

    def add_loops(self, maze, loop_factor=0.1):
        for y in range(1, self.size - 1, 2):
            for x in range(1, self.size - 1, 2):
                if random.random() < loop_factor:
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    random.shuffle(directions)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] == 1:
                            maze[ny][nx] = 0
                            break
        return maze

# Example usage
if __name__ == "__main__":
    size = 21
    wall_thickness = 1
    maze = Maze(size, wall_thickness)
    maze_data = maze.generate_maze()
    maze_data = maze.add_loops(maze_data)

    # Print maze for visual verification
    for row in maze_data:
        print(''.join(['██' if cell == 1 else '  ' for cell in row]))


