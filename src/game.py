import pygame
import random
import time

class SnakeGame:
    # Properties of the game: width, height,
    def __init__(self, board_width: int, board_height: int, enable_graphics: bool):
        self.board_width = board_width
        self.board_height = board_height
        self.grid_size = 20

        self.enable_graphics = enable_graphics
        self.game_display = None
        self.game_surface = None
        self.game_clock = pygame.time.Clock()
        self.snake = Snake(self.board_width, self.board_height)
        self.food = None
        self.score = 0
    def start(self):
        if self.enable_graphics:
            self.init_graphics()

    def init_graphics(self):
        self.game_display = pygame.display.set_mode(
                (self.board_width * self.grid_size, self.board_height * self.grid_size)
            )
        pygame.display.set_caption("Snake Game")
        self.game_surface = pygame.Surface(self.game_display.get_size())
        self.game_surface.convert()

    def draw_grid(self):
        for y in range(0, int(self.board_height)):
            for x in range(0, int(self.board_width)):
                if (x+y)%2 == 0:
                    r = pygame.Rect((x*self.grid_size, y*self.grid_size), (self.grid_size,self.grid_size))
                    pygame.draw.rect(self.game_surface,(93,216,228), r)
                else:
                    rr = pygame.Rect((x*self.grid_size, y*self.grid_size), (self.grid_size,self.grid_size))
                    pygame.draw.rect(self.game_surface, (84,194,205), rr)

    def step(self):
        self.draw_grid()
        self.game_display.blit(self.game_surface, (0, 0))
        pygame.display.update()

    def reset(self):
        self.score = 0
        self.snake = Snake(self.board_width, self.board_height)

class Food:
    def __init__(self, board_width: int, board_height: int):
        self.board_width = board_width
        self.board_height = board_height
        self.x = board_width//2
        self.y = board_height//2
    def new_random_position(self):
        self.x = random.randint(0, self.board_width)
        self.y = random.randint(0, self.board_height)


class Snake:
    def __init__(self, width, height):
        self.x = width//2
        self.y = height//2
        self.direction = None

    def get_position(self):
        return self.x, self.y

    def get_direction(self):
        return self.direction

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
