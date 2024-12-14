from utilities import TwoDimensionalStartIndexArray
from utilities import StartIndexArray
from utilities import ProbabilityVector
from CardBase import get_card_by_id


def draw_cards(player, num_cards):
    # Check if the player has enough cards in the library
    if player.Library.start == 0:
        #TODO: Manage game ends
        #TODO:Create a system for passive effects to trigger. Here we would need to check for cards that prevent a player from loosing the game.
        return
    
    # Draw the specified number of cards
    for _ in num_cards:
        
        drawncardID = player.Library.array[player.Library.start-1]
        player.hand.add(drawncardID)
        player.Library.remove()
        
        Persepective = player.Perspective.Data[player.ID]
        
        ProbabilityofDrawnCard = Persepective["DefaultProbabilityVector"].array[drawncardID]
        if ProbabilityofDrawnCard > 0:
            ProbabilityofDrawnCard -= 1
            
def destroy(player, index):
    CardID = player.Battlefield[0, index]
    Card = get_card_by_id(CardID)
    if Card