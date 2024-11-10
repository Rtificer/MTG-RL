from CardBase import Card
from Abilities.WastesTap import WastesTap
import numpy as np

class Wastes(Card):
    def __init__(self):
        super().__init__(card_id = 1, types = ["Land", "BasicLand"], cost=np.array([0]*6), colors=[7], abilities=[WastesTap])