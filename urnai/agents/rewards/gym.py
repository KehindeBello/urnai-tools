'''
This file is a repository with reward classes for all gym games we've solved.
'''
from urnai.agents.rewards.abreward import RewardBuilder
import numpy as np

class FrozenlakeReward(RewardBuilder):
    def get_reward(self, obs, reward, done):
        if reward == 1:
            return 1000
        elif reward == 0:
            return 1
        else:
            return -1000
