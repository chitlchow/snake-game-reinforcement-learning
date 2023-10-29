import numpy as np
import random

class RLAgent:
    def __init__(self, alpha, gamma , initial_epsilon=1.0):
        self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3))
        self.alpha = alpha
        # Randomness of decision
        self.epsilon = initial_epsilon
        self.epsilon_decay = np.power(0.001/initial_epsilon, 1/10000)
        self.gamma = gamma
        self.history = []
    def update_q_value(self ,current_state, new_state, reward, action):
        self.q_table[current_state][action] = (1 - self.alpha) * self.q_table[current_state][action] + \
                                              self.alpha * (reward + self.gamma * max(self.q_table[new_state]))

    def decision(self, current_state):
        # Make random exploration
        if random.random() < self.epsilon:
            return random.randint(0, 2)
        return np.argmax(self.q_table[current_state])

    def update_epsilon(self):
        self.epsilon *= self.epsilon_decay

    def clear_history(self):
        self.history = []

