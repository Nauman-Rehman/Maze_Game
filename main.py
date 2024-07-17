import pygame
import sys
import time
from maze import Maze
from player import Player
from ai_rat import AIRat
from level import Level

pygame.init()

# Screen settings
screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Rat Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load assets
player_rat_image = pygame.image.load('assets/images/jerry.png')
ai_rat_image = pygame.image.load('assets/images/rat1.png')
cheese_image = pygame.image.load('assets/images/cheese.png')
wall_image = pygame.image.load('assets/images/wall.png')

# Scale images to fit the tile size
def scale_image(image, size):
    return pygame.transform.scale(image, (size, size))

# Game settings
level = Level(size=21)
maze_data = level.get_maze()
tile_size = screen_size // len(maze_data)
player = Player(1, 1)
ai_rats = [AIRat(1, 1) for _ in range(3)]
cheese_position = (len(maze_data) - 2, len(maze_data) - 2)

# AI rat settings
AI_RAT_SPEED = 10  # Lower value means faster movement
AI_RAT_COOLDOWN = 5  # Controls the "vibration" effect

# Scale images
player_rat_image = scale_image(player_rat_image, tile_size)
ai_rat_image = scale_image(ai_rat_image, tile_size)
cheese_image = scale_image(cheese_image, tile_size)
wall_image = scale_image(wall_image, tile_size)

# Font
font = pygame.font.Font(None, 36)

def draw_maze(maze):
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile > 0:  # Wall
                wall_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, BLACK, wall_rect)
                inner_rect = wall_rect.inflate(-tile_size * (1 - tile / level.get_wall_thickness()), -tile_size * (1 - tile / level.get_wall_thickness()))
                screen.blit(wall_image, inner_rect)
            elif (x, y) == cheese_position:
                screen.blit(cheese_image, (x * tile_size, y * tile_size))

def draw_player(player):
    screen.blit(player_rat_image, (player.x * tile_size, player.y * tile_size))

def draw_ai_rats(ai_rats):
    for ai_rat in ai_rats:
        screen.blit(ai_rat_image, (ai_rat.x * tile_size, ai_rat.y * tile_size))

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, BLACK, x + width // 2, y + height // 2)

def main():
    global maze_data, cheese_position, tile_size, ai_rats
    running = True
    clock = pygame.time.Clock()
    game_over = False
    player_won = False
    move_cooldown = 0
    ai_move_counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_pos = pygame.mouse.get_pos()
                if 150 <= mouse_pos[0] <= 250 and 350 <= mouse_pos[1] <= 400:
                    if player_won:
                        maze_data = level.next_level()
                        tile_size = screen_size // level.get_maze_size()
                        player.x, player.y = 1, 1
                        ai_rats = [AIRat(1, 1) for _ in range(3)]
                        cheese_position = (len(maze_data) - 2, len(maze_data) - 2)
                        game_over = False
                        player_won = False
                    else:
                        # Restart current level
                        player.x, player.y = 1, 1
                        ai_rats = [AIRat(1, 1) for _ in range(3)]
                        game_over = False
                elif 350 <= mouse_pos[0] <= 450 and 350 <= mouse_pos[1] <= 400:
                    running = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if move_cooldown == 0:
                if keys[pygame.K_UP]:
                    player.move('UP', maze_data)
                    move_cooldown = 5
                elif keys[pygame.K_DOWN]:
                    player.move('DOWN', maze_data)
                    move_cooldown = 5
                elif keys[pygame.K_LEFT]:
                    player.move('LEFT', maze_data)
                    move_cooldown = 5
                elif keys[pygame.K_RIGHT]:
                    player.move('RIGHT', maze_data)
                    move_cooldown = 5
            else:
                move_cooldown -= 1

            if ai_move_counter == 0:
                for ai_rat in ai_rats:
                    ai_rat.move(maze_data, cheese_position)
                    if (ai_rat.x, ai_rat.y) == cheese_position:
                        game_over = True
                        player_won = False
                        pygame.time.wait(600)  # Wait for 0.6 seconds
                ai_move_counter = AI_RAT_SPEED
            else:
                ai_move_counter -= 1

            if (player.x, player.y) == cheese_position:
                game_over = True
                player_won = True

        screen.fill(WHITE)
        draw_maze(maze_data)
        draw_player(player)
        draw_ai_rats(ai_rats)

        if game_over:
            if player_won:
                draw_text("You Win!", GREEN, screen_size // 2, screen_size // 2 - 50)
                draw_button("Next", GREEN, 150, 350, 100, 50)
            else:
                draw_text("Level Failed", RED, screen_size // 2, screen_size // 2 - 50)
                draw_button("Retry", GREEN, 150, 350, 100, 50)
            draw_button("Quit", RED, 350, 350, 100, 50)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()