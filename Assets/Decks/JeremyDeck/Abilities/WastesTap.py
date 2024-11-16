from AbilityBase import Ability

class WastesTap(Ability):
    def __init__(self):
        super().__init__(ability_id = 4, trigger = "Tap", effect=self.apply_effect)
    
    def apply_effect(self, player):
        player.mana_pool[6] += 1