import os,sys
sys.path.insert(0, os.getcwd())

from absl import app
import gym
from urnai.envs.gym import GymEnv
from urnai.trainers.trainer import Trainer
from urnai.trainers.trainer import TestParams
from urnai.agents.generic_agent import GenericAgent
from urnai.agents.actions.gym_wrapper import GymWrapper
from urnai.agents.rewards.default import PureReward
from urnai.agents.states.gym import PureState
from urnai.agents.states.gym import GymState
from urnai.models.algorithms.dql import DeepQLearning
from urnai.models.dqn_pytorch import DQNPytorch
from urnai.models.ddqn_keras import DDQNKeras
from urnai.models.model_builder import ModelBuilder

def declare_trainer():
    env = GymEnv(id="CartPole-v1", render=True)

    action_wrapper = env.get_action_wrapper()
    state_builder = GymState(env.env_instance.observation_space.shape[0])

    helper = ModelBuilder()
    helper.add_input_layer(nodes=50)
    helper.add_fullyconn_layer(50)
    helper.add_output_layer()

    # dq_network = DeepQLearning(action_wrapper=action_wrapper, state_builder=state_builder, build_model=helper.get_model_layout(), use_memory=False,
    #                     gamma=0.99, learning_rate=0.001, epsilon_decay=0.99995, epsilon_min=0.01, memory_maxlen=50000, min_memory_size=1000, batch_size=64)

    # dq_network = DQNPytorch(action_wrapper=action_wrapper, state_builder=state_builder, build_model=helper.get_model_layout(),
    #                     gamma=0.99, learning_rate=0.001, epsilon_decay=0.9997, epsilon_min=0.01, memory_maxlen=50000, min_memory_size=100)

    dq_network = DDQNKeras(action_wrapper=action_wrapper, state_builder=state_builder, build_model=helper.get_model_layout(), use_memory=False,
                    gamma=0.99, learning_rate=0.001, epsilon_decay=0.999997, epsilon_min=0.01, memory_maxlen=100000, min_memory_size=2000)


    agent = GenericAgent(dq_network, PureReward())

    # Cartpole-v1 is solved when avg. reward over 100 episodes is greater than or equal to 475
    trainer = Trainer(env, agent, save_path='urnai/models/saved', file_name="cartpole_v1_ddqn", 
                    save_every=500, enable_save=True, relative_path=True,
                    max_training_episodes=2000, max_steps_training=1000,
                    max_test_episodes=100, max_steps_testing=1000)
    return trainer

def main(unused_argv):
    try:
        trainer = declare_trainer()
        trainer.train()
        trainer.play()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    app.run(main)
