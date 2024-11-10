from Functions import sacrifice
from AbilityBase import Ability

class SacrificeNonBasicLand(Ability):
    def __init__(self):
        super().__init__(trigger = "Tap", effect=self.apply_effect)
    
    def apply_effect(self, Player, TargetIDs):
        sacrifice(Player[0], TargetIDs[0])