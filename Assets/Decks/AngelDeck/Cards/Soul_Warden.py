from CardBase import Card
from Abilities.SoulWardenPassive import SoulWardenPassive
import numpy as np

class Soul_Warden(Card):
    def __init__(self):
        super().__init__(card_id = 61,  cost={}, types = {"Creature"}, colors=[1], power = 1, toughness = 1, abilities={SoulWardenPassive})