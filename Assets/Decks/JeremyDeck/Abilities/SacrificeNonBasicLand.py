from Functions import sacrifice
from Functions import destroy
from AbilityBase import Ability

class SacrificeNonBasicLand(Ability):
    def __init__(self):
        super().__init__(ability_id = 2, trigger = "Tap", effect=self.apply_effect)
    
    def apply_effect(self, Player, TargetIDs):
        sacrifice(Player[0], TargetIDs[0]) #destroy the card itself
        destroy(Player[1], TargetIDs[1]) # destroy target non-basic land