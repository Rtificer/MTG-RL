import numpy as np
class Deck:
    def __init__(self, librarylist = np.array([0] * 0), CanPlayerObtainOpponentCards = np.bool_(False), CanOpponentObtainPlayerCards = np.bool_(False)):
        self.librarylist = librarylist #CardID To add to the library at the start of the game. Excludes the backs of some cards or tokens that need not be loaded.
        self.CanPlayerObtainOpponentCards = CanPlayerObtainOpponentCards
        self.CanOpponentObtainPlayerCards = CanOpponentObtainPlayerCards