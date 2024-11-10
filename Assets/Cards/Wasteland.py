from CardBase import Card
from Abilities.WastesTap import WastesTap
from Abilities.SacrificeNonBasicLand import SacrificeNonBasicLand
import numpy as np

class WasteLand(Card):
    def __init__(self):
        super().__init__(card_id = 2, types = ["Land"], cost=np.array([0]*6), colors=[7], abilities=[WastesTap, SacrificeNonBasicLand])