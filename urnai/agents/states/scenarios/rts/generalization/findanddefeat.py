from .collectables import CollectablesGeneralizedStatebuilder

class FindAndDefeatGeneralizedStatebuilder(CollectablesGeneralizedStatebuilder):

    def build_drts_map(self, obs): 
        map_ = self.build_basic_drts_map(obs)
        map_ = self.normalize_map(map_)

        return map_
