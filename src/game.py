import pygame
import random
import time

up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)

class SnakeGame:
    """Properties of the game: width, height, graphics and speed of the game"""
    def __init__(self, board_width: int, board_height: int, enable_graphics: bool, game_speed = 10000):
        # Define the game board dimensions
        self.board_width = board_width
        self.board_height = board_height
        self.grid_size = 20

        # Display properties
        self.enable_graphics = enable_graphics
        self.game_speed = game_speed
        self.game_display = None
        self.game_surface = None

        # Game runtime
        self.game_clock = pygame.time.Clock()

        # In-game objects
        self.snake = Snake(self.board_width, self.board_height)
        self.apple = Apple(self.board_width, self.board_height)

        # Game control variables
        self.score = 0
        self.running = False

    def start(self):
        """Function to start the game module"""
        self.running = True     # set running to True
        if self.enable_graphics:    # Enable graphics
            self.init_graphics()


    def init_graphics(self):
        """
        Initialize Graphics component
        """
        # Setup display
        self.game_display = pygame.display.set_mode(
                (self.board_width * self.grid_size, self.board_height * self.grid_size)
            )
        # Display caption
        pygame.display.set_caption(f"Snake Game, Score: {self.score}")
        # Game board surface
        self.game_surface = pygame.Surface(self.game_display.get_size())
        self.game_surface.convert()

    def draw_grid(self):
        """
        Draw the grid of the game
        """
        for y in range(0, int(self.board_height)):
            for x in range(0, int(self.board_width)):
                if (x+y)%2 == 0:
                    r = pygame.Rect((x*self.grid_size, y*self.grid_size), (self.grid_size,self.grid_size))
                    pygame.draw.rect(self.game_surface,(93,216,228), r)
                else:
                    rr = pygame.Rect((x*self.grid_size, y*self.grid_size), (self.grid_size,self.grid_size))
                    pygame.draw.rect(self.game_surface, (84,194,205), rr)

    def move_snake(self):
        """
        Move the snake with its current direction
        """
        # Get the snake position
        current_pos = self.snake.get_head_pos()
        x_dir, y_dir = self.snake.direction
        new_pos = (
            current_pos[0] + x_dir, current_pos[1]+y_dir
        )
        if len(self.snake.positions) > 2 and new_pos in self.snake.positions[2:]:
            return True

        elif new_pos[0] >= self.board_width \
                or new_pos[1] >= self.board_height \
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

    def draw_apple(self):
        """
        Draw the apple with its given position on screen
        :return:
        """
        rect = pygame.Rect((self.apple.position[0]*self.grid_size, self.apple.position[1]*self.grid_size), (self.grid_size, self.grid_size))
        pygame.draw.rect(self.game_surface, self.snake.color, rect)

    def get_states(self):
        """
        Return the current states of the game environment
        :return:
        A tuple consist of 11 state variables, including:
        - Current Directions (4)
        - Dangers nearby (3, relative to the head position)
        - Relative position between the food and the snake (4)

        """
        state = []
        # Current direction as state
        directions = [up, down, left, right]
        for d in directions:
            state.append(int(self.snake.direction == d))

        # Danger as state
        dangers = self.check_dangers()
        state.extend(dangers)

        # relative position for
        rel_pos = self.relative_position()
        state.extend(rel_pos)
        return tuple(state)

    def check_dangers(self):
        """
        Encode dangers as states: front, left and right
        :return: list of 3 integers (either 0 or 1, 0 means none and 1 means there is a close danger in the subsequent direction)
        """
        # head position
        x, y = self.snake.positions[0]

        # False by default for 3 kinds of dangers
        danger_ahead = False
        danger_right = False
        danger_left = False

        actions = [up, right, down, left]
        # Check danger ahead
        front_pos = (x + self.snake.direction[0], y + self.snake.direction[1])
        # If it crash
        if front_pos in self.snake.positions \
                or front_pos[0] >= self.board_width \
                or front_pos[1] >= self.board_height \
                or front_pos[0] < 0 \
                or front_pos[1] < 0:
            danger_ahead = True

        #  Check right
        current_dir_index = actions.index(self.snake.direction)
        right_step = actions[(current_dir_index + 1) % 4]
        right_pos = (x + right_step[0], y + right_step[1])
        if right_pos in self.snake.positions \
                or right_pos[0] >= self.board_width \
                or right_pos[1] >= self.board_height \
                or right_pos[0] < 0 \
                or right_pos[1] < 0:
            danger_right = True

        # Check left
        left_step = actions[(current_dir_index - 1) % 4]
        left_pos = (x + left_step[0], y + left_step[1])

        if left_pos in self.snake.positions \
                or left_pos[0] >= self.board_width \
                or left_pos[1] >= self.board_height \
                or left_pos[0] < 0 \
                or left_pos[1] < 0:
            danger_left = True

        dangers = [int(danger_ahead), int(danger_right), int(danger_left)]
        return dangers

    def relative_position(self):
        """
        Check the relative position of the apple on the board
        :return:
        """
        head_pos = self.snake.positions[0]
        food_pos = self.apple.position

        # Compute the difference in coordinates
        delta_x = head_pos[0] - food_pos[0]
        delta_y = head_pos[0] - food_pos[0]

        # Prepare variables
        food_up = False
        food_down = False
        food_right = False
        food_left = False

        if delta_x < 0:
            food_right = True
            food_left = False
        elif delta_x > 0:
            food_right = False
            food_left = True
        if delta_y > 0:
            food_up = False
            food_down = True
        elif delta_y < 0:
            food_up = True
            food_down = False

        return [int(food_up), int(food_down), int(food_right), int(food_left)]

    def step(self):
        """
        Proceed the game with all other steps
        :return: Reward of action determine by the environment state
        """
        # Move the snake
        crash = self.move_snake()
        if crash:
            # -10 reward if crashed
            self.running = False
            reward = -10
        elif self.scored():
            # 1 reward if scored
            self.score += 1
            reward = 1
            pygame.display.set_caption(f"Snake Game, Score: {self.score}")
        else:
            # 0 reward if nothing happened
            reward = 0
        # Execute if graphics is enabled
        if self.enable_graphics:
            self.draw_grid()
            self.draw_snake()
            self.draw_apple()
            self.game_display.blit(self.game_surface, (0, 0))
            pygame.display.update()
        # Turn the clock
        self.game_clock.tick(self.game_speed)
        return reward

    def reset(self):
        """
        Reset the game
        """
        self.running = False
        self.score = 0
        pygame.display.set_caption(f"Snake Game, Score: {self.score}")
        self.snake.reset()
        self.apple.new_random_position()


    def scored(self):
        """Determine if the snake has scored"""
        if self.snake.positions[0] == self.apple.position:
            self.apple.new_random_position()
            self.snake.length += 1
            return True
        return False

class Apple:
    def __init__(self, board_width: int, board_height: int):
        self.board_width = board_width
        self.board_height = board_height
        self.position = (random.randint(0, board_width - 1),random.randint(0, board_height - 1))
        self.color = (223, 163, 49)

    def new_random_position(self):
        self.position = (random.randint(0, self.board_width - 1),random.randint(0, self.board_height - 1))

class Snake:
    def __init__(self, board_width: int, board_height: int):
        self.board_width = board_width
        self.board_height = board_height
        self.direction = random.choice([up, down, right, left])
        self.positions = [(board_width//2, board_height//2)]
        self.color = (17, 24, 47)
        self.length = 1

    def get_position(self):
        return self.positions

    def get_direction(self):
        return self.direction

    def get_head_pos(self):
        return self.positions[0]

    def turn(self, action):
        turn_dict = {
            0: "turn_right",
            1: "turn_left",
            2: "forward"
        }
        action = turn_dict[action]
        # Set direction if turning right
        if action == 'turn_right':
            if self.direction == up:
                self.direction = right
            elif self.direction == down:
                self.direction = left
            elif self.direction == right:
                self.direction = down
            elif self.direction == left:
                self.direction = up
        # Turning Left
        elif action == 'turn_left':
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

    def reset(self):
        self.positions = [(self.board_width//2, self.board_height//2)]
        self.length = 1


