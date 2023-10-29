import numpy as np
import random
from torch import nn
import torch
import numpy as np


class QLAgent:
    def __init__(self, alpha = 0.001, gamma=0.99, initial_epsilon=1.0):
        """
        :param alpha: Learning rate of the Q-Learning algorithm, default is 0.001
        :param gamma: Discount rate of reward, default is 0.99
        :param initial_epsilon: The initial value for epsilon (exploration parameter), default is 1.0
        """
        self.q_table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3))

        # Randomness of decision
        self.epsilon = initial_epsilon
        self.epsilon_decay = np.power(0.001/initial_epsilon, 1/10000)

        self.gamma = gamma

        self.alpha = alpha
        # self.alpha_0 = alpha
        # self.alpha_decay = 0.0012

    def update_q_value(self ,current_state, new_state, reward, action):
        """
        Update the q-value using the Bellman's equation

        :param current_state: the current state of the environment, a tuple of 11 values
        :param new_state: The next state after performing an action
        :param reward: Reward given by the environment
        :param action: Action took by the agent

        """
        self.q_table[current_state][action] = (1 - self.alpha) * self.q_table[current_state][action] + \
                                              self.alpha * (reward + self.gamma * max(self.q_table[new_state]))

    def decision(self, current_state):
        """
        Function for making decision based on the current state, retrieve by taking the argument max value of the state-transition vector
        :param current_state: The state vector with 11 integer values
        :return: The argument max of the vector of the q-values of that state
        """
        if random.random() < self.epsilon:
            return random.randint(0, 2)
        return np.argmax(self.q_table[current_state])

    def update_epsilon(self):
        """
        Update the epsilon by multiplying it with the epsilon decay
        """
        self.epsilon *= self.epsilon_decay

    # def update_alpha(self, ep):
    #     """Learning rate scheduling using exponential decay"""
    #     self.alpha = self.alpha_0 * np.exp(-self.alpha_decay*ep)