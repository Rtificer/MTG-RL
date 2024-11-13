from CardBase import Card
from Abilities.WastesTap import WastesTap
import numpy as np

class Wastes(Card):
    def __init__(self):
        super().__init__(card_id = 3,  cost=np.array([0, 0, 0, 0, 0, 1], types = ["Artifact"], dtype=np.uint8), colors=[7], power = None, toughness = None, abilities=[WastesTap])