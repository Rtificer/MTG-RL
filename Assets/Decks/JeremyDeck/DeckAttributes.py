from DeckBase import Deck
import numpy as np

class JeremyDeck(Deck):
    def __init__(self):
        super().__init__(    
            librarylist = np.array(1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3),
            CanPlayerObtainOpponentCards = np.bool_(False),
            CanOpponentObtainPlayerCards = np.bool_(False)
        )