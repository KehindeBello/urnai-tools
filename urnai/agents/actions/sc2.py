import random
from pysc2.lib import actions, features


'''
An action set defines all actions an agent can use. In the case of StarCraft 2 using PySC2, some actions require extra
processing to work, so it's up to the developper to come up with a way to make them work.

Even though this is not called action_wrapper, this actually acts as a wrapper

e.g: select_point is a function implemented in PySC2 that requires some extra arguments to work, like which point to select.
Using the action_set we can define a way to select which point select_point will use.
Following this example, we could implement a select_random_unit function which processes a random unit from the observation
and returns the corresponding PySC2 call to select_point that would select this processed unit.

'''

## TODO: Move constants to a separate file, so they can be imported and used by other modules
## Defining constants for action ids, so our agent can check if an action is valid
_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id
_HARVEST_GATHER = actions.FUNCTIONS.Harvest_Gather_screen.id

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_PLAYER_ID = features.SCREEN_FEATURES.player_id.index

_PLAYER_SELF = 1
_PLAYER_HOSTILE = 4
_ARMY_SUPPLY = 5

_TERRAN_COMMANDCENTER = 18
_TERRAN_SUPPLY_DEPOT = 19
_TERRAN_BARRACKS = 21
_TERRAN_SCV = 45
_NEUTRAL_MINERAL_FIELD = 341

_NOT_QUEUED = [0]
_QUEUED = [1]
_SELECT_ALL = [2]


def no_op():
    return actions.FUNCTIONS.no_op()


def select_random_unit(obs):
    unit_type = obs.feature_screen[_UNIT_TYPE]
    unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()

    if unit_y.any():
        i = random.randint(0, len(unit_y) - 1)
        target = [unit_x[i], unit_y[i]]

        return actions.FUNCTIONS.select_point(_NOT_QUEUED, target)
    
    return actions.FUNCTIONS.no_op()


def select_all_barracks(obs):
    unit_type = obs.feature_screen[_UNIT_TYPE]
    barracks_y, barracks_x = (unit_type == _TERRAN_BARRACKS).nonzero()

    if barracks_y.any():
        i = random.randint(0, len(barracks_y) - 1)
        target = [barracks_x[i], barracks_y[i]]

        return actions.FUNCTIONS.select_point(_SELECT_ALL, target)

    return actions.FUNCTIONS.no_op()


def select_army(obs):
    if _SELECT_ARMY in obs.available_actions:
        return actions.FUNCTIONS.select_army(_NOT_QUEUED)
    return actions.FUNCTIONS.no_op()


def build_supply_depot(obs, target):
    if _BUILD_SUPPLY_DEPOT in obs.available_actions:
        return actions.FUNCTIONS.Build_SupplyDepot_screen(_NOT_QUEUED, target)
    return actions.FUNCTIONS.no_op()


def build_barracks(obs, target):
    if _BUILD_BARRACKS in obs.available_actions:
        return actions.FUNCTIONS.Build_Barracks_screen(_NOT_QUEUED, target)
    return actions.FUNCTIONS.no_op()


def train_marine(obs):
    if _TRAIN_MARINE in obs.available_actions:
        return actions.FUNCTIONS.Train_Marine_quick(_QUEUED)
    return actions.FUNCTIONS.no_op()


def attack_target_point(obs, target):
    if _ATTACK_MINIMAP in obs.available_actions:
        return actions.FUNCTIONS.Attack_minimap(_NOT_QUEUED, target)
    return actions.FUNCTIONS.no_op()


def harvest_point(obs):
    if _HARVEST_GATHER in obs.available_actions:
        unit_type = obs.feature_screen[_UNIT_TYPE]
        unit_y, unit_x = (unit_type == _NEUTRAL_MINERAL_FIELD).nonzero()

        if unit_y.any():
            i = random.randint(0, len(unit_y) - 1)

            m_x = unit_x[i]
            m_y = unit_y[i]

            target = [int(m_x), int(m_y)]

            return actions.FUNCTIONS.Harvest_Gather_screen(_QUEUED, target)
    return actions.FUNCTIONS.no_op()
