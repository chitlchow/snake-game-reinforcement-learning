from src.game import SnakeGame
import time
import pygame

def main():
    game = SnakeGame(40, 20, enable_graphics=True)
    game.start()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()