from CardBase import Card
from Abilities.WastesTap import WastesTap
import numpy as np

class Wastes(Card):
    def __init__(self):
        super().__init__(card_id = 1, cost=np.array([0]*6), types = ["Land", "BasicLand"], colors=[7], power = None, toughness = None, abilities=[WastesTap])