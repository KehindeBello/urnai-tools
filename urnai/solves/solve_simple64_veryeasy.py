import os,sys
sys.path.insert(0, os.getcwd())

from absl import app

from urnai.envs.sc2 import SC2Env
from urnai.trainers.trainer import Trainer
from urnai.agents.sc2_agent import SC2Agent
from urnai.agents.actions.sc2_wrapper import SimpleTerranWrapper
from urnai.agents.rewards.sc2 import KilledUnitsReward
from urnai.agents.states.sc2 import Simple64GridState
from urnai.models.ddqn_keras import DDQNKeras
from urnai.models.model_builder import ModelBuilder

def main(unused_argv):
    try:
        env = SC2Env(map_name="Simple64", render=False, 
                     step_mul=16, player_race="terran", 
                     enemy_race="random", difficulty="very_easy")
        
        action_wrapper = SimpleTerranWrapper()
        state_builder = Simple64GridState(grid_size=4)
        
        helper = ModelBuilder()
        helper.add_input_layer(nodes=50)
        helper.add_fullyconn_layer(50)
        helper.add_output_layer()

        dq_network = DDQNKeras(action_wrapper=action_wrapper, 
                               state_builder=state_builder, 
                               build_model=helper.get_model_layout(), 
                               per_episode_epsilon_decay=False,
                                gamma=0.99, learning_rate=0.001, 
                               epsilon_decay=0.99999, epsilon_min=0.005, 
                               memory_maxlen=100000, min_memory_size=2000)
        
        agent = SC2Agent(dq_network, KilledUnitsReward())
        

        trainer = Trainer(env, agent, save_path='urnai/models/saved', file_name="terran_ddqn_vs_random_v_easy", 
                        save_every=50, enable_save=True, relative_path=True,
                        max_training_episodes=3000, max_steps_training=1200,
                        max_test_episodes=100, max_steps_testing=1200)
        trainer.train()
        trainer.play()


    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    app.run(main)
