from urnai.scenarios.generalization.rts.defeatenemies import GeneralizedDefeatEnemiesScenario as Scenario
#from urnai.scenarios.generalization.rts.buildunits import GeneralizedBuildUnitsScenario as Scenario
#from urnai.scenarios.generalization.rts.findanddefeat import GeneralizedFindaAndDefeatScenario as Scenario
#from urnai.scenarios.generalization.rts.collectables import GeneralizedCollectablesScenario as Scenario
import numpy as np
import sys

episodes = 100
steps = 99999999999 

env = Scenario(game = Scenario.GAME_STARCRAFT_II, render = True)
action_wrapper = env.get_default_action_wrapper()
np.set_printoptions(threshold=sys.maxsize)

np.set_printoptions(threshold=sys.maxsize)

for ep in range(episodes):
    reward = 0
    done = False
    state = env.reset()
    print("Episode " + str(ep + 1))
    
    for step in range(steps):
            print("Step " + str(step + 1))
            
            text = '''
                Choose:
                    1 - Left 
                    2 - Right 
                    3 - Up 
                    4 - Down 
                    5 - Attack Nearest Unit 
                    6 - Run 
                    7 - Stop 
                    8 - No-Op
            '''

            action = None

            try:
                action = int(input(text))
            except ValueError:
                action = 8

            action -= 1
            action = action_wrapper.get_action(action, state)

            state, reward, done = env.step(action)

            print("Map shape: {}".format(state.feature_minimap[4].shape))
            print("Map: {}".format(state.feature_minimap[4]))

            print("Reward: {r}".format(r=reward))

            if done: break
