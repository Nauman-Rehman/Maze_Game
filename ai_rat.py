import random
from collections import deque

class AIRat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = []
        self.visited = set()

    def move(self, maze, target):
        if not self.path:
            self.explore(maze, target)
        if self.path:
            next_move = self.path.pop(0)
            self.x, self.y = next_move
            self.visited.add((self.x, self.y))

    def explore(self, maze, target):
        possible_moves = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = self.x + dx, self.y + dy
            if (0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and
                maze[new_y][new_x] == 0 and (new_x, new_y) not in self.visited):
                possible_moves.append((new_x, new_y))

        if possible_moves:
            next_move = random.choice(possible_moves)
            self.path = [next_move]
        else:
            # Backtrack
            self.visited.clear()
            self.path = self.find_path(maze, (self.x, self.y), target)[:5]  # Only take first 5 steps

    def find_path(self, maze, start, goal):
        queue = deque([start])
        visited = set([start])
        parent_map = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                break

            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if (0 <= neighbor[0] < len(maze[0]) and 0 <= neighbor[1] < len(maze) and
                        maze[neighbor[1]][neighbor[0]] == 0 and neighbor not in visited):
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent_map[neighbor] = current

        path = []
        step = goal
        while step:
            path.append(step)
            step = parent_map.get(step)
        path.reverse()
        return path