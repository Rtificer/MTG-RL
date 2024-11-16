from DeckBase import Deck
import numpy as np

class AngelDeck(Deck):
    def __init__(self):
        super().__init__(    
            librarylist = {61, 61, 61, 61},
            CanPlayerObtainOpponentCards = np.bool_(False),
            CanOpponentObtainPlayerCards = np.bool_(False)
        )