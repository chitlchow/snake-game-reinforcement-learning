from src.game import SnakeGame
import time
import pygame

def main():
    game = SnakeGame(20, 20, enable_graphics=True)
    game.start()
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.reset()
        game.step()

if __name__ == "__main__":
    main()