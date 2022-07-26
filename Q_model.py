import numpy as np
import random

class Q_model:
    def __init__(self, num_states, num_actions):
        self.q_table = np.zeros((num_states, num_actions))
        self.epsilon = 0.1
        self.alpha = 0.1
        self.gamma = 0.4

    def check_explore(self):
        if random.uniform(0, 1) < self.epsilon:
            return True
        return False

    def update_table(self, state, action, reward, new_state):
        self.q_table[state, action] = (1 - self.alpha) * self.q_table[state, action] \
                                        + self.alpha * (reward + self.gamma * np.argmax(self.q_table[new_state]) - self.q_table[state, action]) 
    
    def best_action(self, state):
        return np.argmax(self.q_table[state])
                                        

