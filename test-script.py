from src.game import SnakeGame
from src.agent import RLAgent
import pickle
import numpy as np
import pygame
game = SnakeGame(20, 20, enable_graphics=True, game_speed=10)
enable_update = True

with open('pickles/q-tables-highest-score-54.pkl', 'rb') as f:
    params = pickle.load(f)
    agent = RLAgent(alpha=params['alpha'], gamma=params['gamma'])
    agent.epsilon = 0
    agent.q_table = params['q_table']

while True:
    game.start()
    while game.running:
        if game.enable_graphics:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.reset()
        current_state = game.get_states()
        action = agent.decision(current_state)
        game.snake.turn(action)
        reward = game.step()
        new_state = game.get_states()
        if enable_update:
            agent.update_q_value(current_state, new_state, reward, action)
    print(game.score)
    game.reset()




