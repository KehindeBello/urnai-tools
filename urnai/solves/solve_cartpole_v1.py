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
from urnai.models.dqn_keras import DQNKeras
from urnai.models.ddqn_keras import DDQNKeras
from urnai.models.pg_keras import PGKeras
from urnai.models.model_builder import ModelBuilder

def main(unused_argv):
    try:
        env = GymEnv(id="CartPole-v1")

        action_wrapper = env.get_action_wrapper()
        state_builder = GymState(env.env_instance.observation_space.shape[0])

        helper = ModelBuilder()
        helper.add_input_layer(nodes=50)
        helper.add_fullyconn_layer(50)
        helper.add_output_layer()

        dq_network = DDQNKeras(action_wrapper=action_wrapper, state_builder=state_builder, build_model=helper.get_model_layout(), use_memory=False,
                            gamma=0.99, learning_rate=0.001, epsilon_decay=0.9997, epsilon_min=0.01, memory_maxlen=50000, min_memory_size=1000)

        # dq_network = PGKeras(action_wrapper, state_builder, learning_rate=0.001, gamma=0.99, build_model=helper.get_model_layout())

        agent = GenericAgent(dq_network, PureReward())

        # Cartpole-v1 is solved when avg. reward over 100 episodes is greater than or equal to 475
        #test_params = TestParams(num_matches=100, steps_per_test=100, max_steps=500, reward_threshold=500)
        trainer = Trainer(env, agent, save_path='urnai/models/saved', file_name="cartpole_v1_ddqn_50x50_test", 
                        save_every=100, enable_save=True, relative_path=True,
                        max_training_episodes=1000, max_steps_training=500,
                        max_test_episodes=100, max_steps_testing=500)
        trainer.train()
        trainer.play()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    app.run(main)
