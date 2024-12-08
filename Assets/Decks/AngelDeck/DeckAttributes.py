from DeckBase import Deck
import numpy as np

class AngelDeck(Deck):
    def __init__(self):
        super().__init__(    
            librarylist = np.array(61, 61, 61, 61),
            totalcardcount = 4
        )