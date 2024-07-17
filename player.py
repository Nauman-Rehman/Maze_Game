class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction, maze):
        new_x, new_y = self.x, self.y
        if direction == 'UP':
            new_y -= 1
        elif direction == 'DOWN':
            new_y += 1
        elif direction == 'LEFT':
            new_x -= 1
        elif direction == 'RIGHT':
            new_x += 1

        if (0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and
            maze[new_y][new_x] == 0):
            self.x, self.y = new_x, new_y

