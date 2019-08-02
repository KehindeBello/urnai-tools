from absl import app
from envs.gym import GymEnv
from envs.trainer import Trainer
from envs.trainer import TestParams
from agents.generic_agent import GenericAgent
from agents.actions.gym_wrapper import GymWrapper
from agents.rewards.default import PureReward
from agents.states.gym import PureState
from models.pg_tf import PolicyGradientTF

def main(unused_argv):
    trainer = Trainer()

    try:
        env = GymEnv(id="CartPole-v0")

        action_wrapper = GymWrapper(env)
        state_builder = PureState(env)

        dq_network = PolicyGradientTF(action_wrapper, state_builder, 'urnai/models/saved/cartpole_v0_pg', learning_rate=0.01, gamma=0.9)

        agent = GenericAgent(dq_network, PureReward())

        # Cartpole-v0 is solved when avg. reward over 100 episodes is greater than or equal to 195
        test_params = TestParams(num_matches=100, steps_per_test=200, max_steps=1000, reward_threshold=200)
        trainer.train(env, agent, num_episodes=2000, max_steps=1000, save_steps=1000, test_params=test_params, enable_save=False)
        trainer.play(env, agent, num_matches=100, max_steps=1000)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    app.run(main)