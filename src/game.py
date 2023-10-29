import pygame
import random
import time

up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)

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
        self.apple = Apple(self.board_width, self.board_height)

        self.score = 0
        self.running = False
    def start(self):
        self.running = True
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

    def move_snake(self):
        current_pos = self.snake.get_head_pos()
        x_dir, y_dir = self.snake.direction
        new_pos = (
            current_pos[0] + x_dir, current_pos[1]+y_dir
        )
        if len(self.snake.positions) > 2 and new_pos in self.snake.positions[2:]:
            return True

        elif new_pos[0] > self.board_width \
                or new_pos[1] > self.board_height \
                or new_pos[0] < 0 \
                or new_pos[1] < 0:
            return True
        else:
            self.snake.positions.insert(0, new_pos)
            if len(self.snake.positions) > self.snake.length:
                self.snake.positions.pop()
        return False

    def draw_snake(self):
        for p in self.snake.positions:
            r = pygame.Rect((p[0]*self.grid_size, p[1]*self.grid_size), (self.grid_size, self.grid_size))
            pygame.draw.rect(self.game_surface, self.snake.color, r)
            pygame.draw.rect(self.game_surface, (93, 216, 228), r, 1)
    def draw_food(self):
        rect = pygame.Rect((self.apple.position[0]*self.grid_size, self.apple.position[1]*self.grid_size), (self.grid_size, self.grid_size))
        pygame.draw.rect(self.game_surface, self.snake.color, rect)

    def get_states(self):
        states = []
        directions = [up, down, left, right]
        for d in directions:
            states.append(int(self.snake.direction == d))


        return states

    def check_dangers(self):
        x, y = self.snake.get_head_pos()

    def step(self):
        # Actions

        crash = self.move_snake()
        self.draw_grid()
        self.draw_snake()
        self.draw_food()
        self.game_display.blit(self.game_surface, (0, 0))
        if crash:
            self.running = False
        pygame.display.update()
        self.game_clock.tick(10)

    def reset(self):
        self.running = False
        self.score = 0
        self.snake = Snake(self.board_width, self.board_height)

class Apple:
    def __init__(self, board_width: int, board_height: int):
        self.board_width = board_width
        self.board_height = board_height
        self.position = (random.randint(0, board_width),random.randint(0, board_height))
        self.color = (223, 163, 49)

    def new_random_position(self):
        self.position = (random.randint(0, self.board_width),random.randint(0, self.board_height))


class Snake:
    def __init__(self, width, height):
        self.x = width//2
        self.y = height//2
        self.direction = random.choice([up, down, right, left])
        self.positions = [((width/2), (height/2))]
        self.color = (17, 24, 47)
        self.length = 1
    def get_position(self):
        return self.positions

    def get_direction(self):
        return self.direction
    def get_head_pos(self):
        return self.positions[0]

    def turn(self, direction):
        # Turning Right
        if direction == 'turn_right':
            if self.direction == up:
                self.direction = right
            elif self.direction == down:
                self.direction = left
            elif self.direction == right:
                self.direction = down
            elif self.direction == left:
                self.direction = up
        # Turning Left
        elif direction == 'turn_left':
            if self.direction == up:
                self.direction = left
            elif self.direction == left:
                self.direction = down
            elif self.direction == down:
                self.direction = right
            elif self.direction == right:
                self.direction = up
        # Going forward (doing noting)
        else:
            self.direction

