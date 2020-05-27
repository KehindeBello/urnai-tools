import warnings
import numpy as np
from .abstate import StateBuilder
from envs.base.abenv import Env

class FrozenLakeState(StateBuilder):
    def build_state(self, obs):
        if obs != None:
            index = obs
            obs = np.zeros((1, 16))
            obs[0][index] = 1
            return obs
        else:
            return None

    def get_state_dim(self):
        return 16


class Game2048State(StateBuilder):
    def __init__(self, env: Env, state_dimension_height, state_dimension_width):
        self.state_dim = env.env_instance.height*env.env_instance.width
        self.state_dim = state_dimension_height*state_dimension_width

    def build_state(self, obs):
        obs = obs.reshape(1, self.get_state_dim())
        return obs

    def get_state_dim(self):
        return self.state_dim


class PureState(StateBuilder):
    def __init__(self, state_dim):
        #you can get observation_space from gym_env.env_instance.observation_space.shape[0]
        self.state_dim = state_dim 

    def preprocess_obs(self, obs):
        if type(obs) == int:
            new_obs = np.array(obs)
            new_obs = new_obs.reshape(1, self.get_state_dim())
            return new_obs
        else:
            return obs.reshape(1, self.get_state_dim())

    def build_state(self, obs):
        # self.preprocess_obs(obs)
        obs = self.preprocess_obs(obs)
        return obs

    def get_state_dim(self):
        return self.state_dim

class GymState(StateBuilder):
    def __init__(self, state_dim):
        #you can get observation_space from gym_env.env_instance.observation_space.shape[0]
        self.state_dim = env.env_instance.observation_space.shape[0]

    def build_state(self, obs):
        state = obs[np.newaxis, :]
        return state

    def get_state_dim(self):
        return self.state_dim
