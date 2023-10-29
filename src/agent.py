import numpy as np
import random

class RLAgent:
    def __init__(self):
        self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3))
        self.alpha = 0.002
        self.epsilon = 0.99
        self.epsilon_decay = 0.99
        self.beta = 0.8

    def update(self, current_state, reward):
        self.q_table[current_state] =
    def decision(self, current_state):
        if random.random() > self.epsilon:
            return np.argmax(self.q_table[current_state])
        return random.randint(0, 2)

