from AbilityBase import Ability

class SolRingTap(Ability):
    def __init__(self):
        super().__init__(ability_id = 3, trigger = "Tap", effect=self.apply_effect)
    
    def apply_effect(self, player):
        player.mana_pool[6] += 2