from AbilityBase import Ability

class SoulWardenPassive(Ability):
    def __init__(self):
        super().__init__(ability_id = 2, trigger = "Passive", effect=self.apply_effect)
    
    def apply_effect(self, Player, TargetIDs):
        #TODO: passive effects not implemented yet
        print("passive effects not implemented yet")