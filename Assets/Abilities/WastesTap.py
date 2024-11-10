from AbilityBase import Ability

class WastesTap(Ability):
    def __init__(self):
        super().__init__(trigger = "Tap", effect=self.apply_effect)
    
    def apply_effect(self, player):
        player.mana_pool[6] += 1