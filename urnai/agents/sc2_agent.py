from abc import abstractmethod
from pysc2.lib import actions, features
from models.base.abmodel import LearningModel
from .base.abagent import Agent
from models.base.abmodel import LearningModel
from agents.rewards.abreward import RewardBuilder

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_SELF = 1

class SC2Agent(Agent):
    def __init__(self, model: LearningModel, reward_builder: RewardBuilder, env):
        super(SC2Agent, self).__init__(model, reward_builder)
        self.setup(env)
        self.reward = 0
        self.episodes = 0
        self.steps = 0
        self.obs_spec = None
        self.action_spec = None

    def setup(self, env):
        self.obs_spec = env.env_instance.observation_spec()
        self.action_spec = env.env_instance.action_spec()

    def reset(self):
        super(SC2Agent, self).reset()
        self.episodes += 1

    def step(self, obs, reward, done):
        self.steps += 1
        self.reward += reward

        if done:
            self.reset()
            return [actions.FUNCTIONS.no_op()]

        if self.action_wrapper.is_action_done():
            ## Building our agent's state
            current_state = self.build_state(obs)

            excluded_actions = self.action_wrapper.get_excluded_actions(obs)
            predicted_action_idx = self.model.choose_action(current_state, excluded_actions)

            self.previous_action = predicted_action_idx
            self.previous_state = current_state
        return [self.action_wrapper.get_action(self.previous_action, obs)]

    def play(self, obs):
        if self.action_wrapper.is_action_done():
            current_state = self.build_state(obs)
            predicted_action_idx = self.model.predict(current_state)
            self.previous_action = predicted_action_idx
        return [self.action_wrapper.get_action(self.previous_action, obs)]