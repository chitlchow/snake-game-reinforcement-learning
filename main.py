from src.game import SnakeGame
from src.agent import RLAgent

import pandas as pd
import numpy as np
import time
import pickle
import pygame
import os

# Clear the pickles directory
pickles_dir = 'pickles'
for f_name in os.listdir(pickles_dir):
    f_path = os.path.join(pickles_dir, f_name)
    if os.path.isfile(f_path):
        os.remove(f_path)

def main():
    results = []
    steps_timeout = 1000
    num_episodes = 10000
    final_epsilon = 0.001
    agent = RLAgent(alpha=0.01, gamma=0.99, initial_epsilon=1.0)

    agent.epsilon_decay = np.power(final_epsilon/agent.epsilon, 1/num_episodes)
    print(f"Using epsilon decay: {agent.epsilon_decay}")
    game = SnakeGame(20, 20, enable_graphics=False)
    highest_score = 0
    for ep in range(num_episodes):
        game.start()
        steps = 0
        steps_without_score = 0
        while game.running:
            steps += 1
            if steps_without_score < steps_timeout:
                if game.enable_graphics:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game.reset()
                # Retrieve the current state of the game

                current_state = game.get_states()
                action = agent.decision(current_state)
                game.snake.turn(action)

                reward = game.step()
                if reward == 0:
                    steps_without_score += 1
                else:
                    # reset the timeout counter
                    steps_without_score = 0
                new_state = game.get_states()
                agent.update_q_value(current_state, new_state, reward, action)
            else:
                game.running = False
        # When there are new records
        if game.score > highest_score:
            highest_score = game.score
            with open(f'pickles/q-tables-highest-score-{game.score}.pkl', 'wb') as f:
                params = {
                    "q_table": agent.q_table,
                    "alpha": agent.alpha,
                    "gamma": agent.gamma
                }
                pickle.dump(params, f)


        result = {"episode": ep, "score": game.score, "epsilon": agent.epsilon, "steps": steps}
        print(result)
        agent.update_epsilon()
        game.reset()
        results.append(result)
    result_df = pd.DataFrame(results)
    result_df.to_csv("result/q-learning-result.csv", index=None)



if __name__ == "__main__":
    main()