from CardBase import Card
from ..Abilities.SolRingTap import SolRingTap

class Soul_Ring(Card):
    def __init__(self):
        super().__init__(card_id = 3,  cost={}, types = {"Artifact"}, colors={7}, power = None, toughness = None, abilities={SolRingTap})