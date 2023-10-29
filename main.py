from src.game import SnakeGame
from src.agent import QLAgent

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
    # List for storing the result
    results = []

    # Environment settings
    # End episode if the agent earning nothing in 1000 stepsd
    steps_timeout = 1000
    # Total number of episodes training
    num_episodes = 10000
    # Target epsilon in the final episode
    final_epsilon = 0.001

    # Initialize Q-learning agent
    agent = QLAgent(alpha=0.01, gamma=0.99, initial_epsilon=1.0)

    agent.epsilon_decay = np.power(final_epsilon/agent.epsilon, 1/num_episodes)
    print(f"Using epsilon decay: {agent.epsilon_decay}")
    game = SnakeGame(10, 10, enable_graphics=False)
    highest_score = 0
    for ep in range(num_episodes):
        # Start the game
        game.start()
        steps = 0
        steps_without_score = 0

        # Game loop
        while game.running:

            steps += 1
            if steps_without_score < steps_timeout:
                if game.enable_graphics:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game.reset()

                # Retrieve the current state of the game
                current_state = game.get_states()
                # Agent make decision
                action = agent.decision(current_state)
                # Deploy action
                game.snake.turn(action)
                # Check reward given
                reward = game.step()

                if reward == 0:
                    steps_without_score += 1
                elif reward == 1:
                    # reset the timeout counter
                    steps_without_score = 0
                else:
                    steps_without_score += 1
                    end_reason = "crash"
                new_state = game.get_states()
                agent.update_q_value(current_state, new_state, reward, action)
            else:
                game.running = False
                end_reason = "timeout"
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

        result = {"episode": ep+1, "score": game.score, "epsilon": agent.epsilon, "steps": steps, "alpha": agent.alpha, "end_reason": end_reason}
        print(result)

        # perform epsilon decay
        agent.update_epsilon()
        # Reset game
        game.reset()
        # Store the result
        results.append(result)

    # Create a dataframe for result analysis
    result_df = pd.DataFrame(results)
    # Save the DF to result folder
    result_df.to_csv("result/q-learning-result.csv", index=None)

if __name__ == "__main__":
    main()