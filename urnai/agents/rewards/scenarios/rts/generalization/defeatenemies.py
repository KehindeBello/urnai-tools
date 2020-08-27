from .findanddefeat import FindAndDefeatGeneralizedRewardBuilder 

class DefeatEnemiesGeneralizedRewardBuilder(FindAndDefeatGeneralizedRewardBuilder):

    def get_sc2_reward(self, obs):
        current = self.get_sc2_number_of_roaches(obs)
        prev = self.get_sc2_number_of_roaches(self.previous_state)

        rwdA = current - prev * 1000

        current = self.get_sc2_number_of_marines(obs)
        prev = self.get_sc2_number_of_marines(self.previous_state)

        rwdB = current - prev * 1000

        return rwdB - rwdA * 1000
