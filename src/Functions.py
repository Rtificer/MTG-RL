import numpy as np
import sys
import os
import importlib
from CardBase import Card, register_card
from AbilityBase import register_ability
from utils.utils import obtainpositiveinteger
from DeckBase import Deck

def register_decks():
    # Add Decks directory to sys.path
    decks_path = os.path.join(os.getcwd(), "Assets", "Decks")
    sys.path.append(decks_path)

    deck_data = {}

    # Get a list of deck directories or files (assuming directories for modularity)
    decks = [deck for deck in os.listdir(decks_path) if os.path.isdir(os.path.join(decks_path, deck))]
    
    for deck in decks:
        print(f"Processing deck: {deck}")
        
        deck_module_name = f"{deck}.DeckAttributes"
        
        try:
            # Import the deck module and extract attributes
            deck_module = importlib.import_module(deck_module_name)
            deck_instance = deck_module.Deck()  # Create an instance of the Deck class
            
            librarylist = getattr(deck_instance, 'librarylist', None)
            totalcardcount = getattr(deck_instance, 'totalcardcount', None)
            
            # Store data in the dictionary
            deck_data[deck] = {
                "librarylist": librarylist,
                "totalcardcount": totalcardcount,
            }
            
            print(f"Data for {deck}: {deck_data[deck]}")
        
        except ModuleNotFoundError as e:
            print(f"Module {deck_module_name} not found: {e}")
        except Exception as e:
            print(f"Error processing deck {deck}: {e}")
    
    return deck_data


def register_cards():

    # Add Decks path to sys.path
    decks_path = os.path.join(os.getcwd(), "Assets", "Decks")
    sys.path.append(decks_path)

    Decks = os.listdir(decks_path)
    for deck in Decks:

        # Process card files
        cards_dir = os.path.join(decks_path, deck, "Cards")
        for filename in os.listdir(cards_dir):
            if filename != '__init__.py' and not filename.startswith('__pycache__'):
                print(f"Processing card file: {filename}")
                module_name = f"{deck}.Cards.{filename[:-3]}"

                try:
                    module = importlib.import_module(module_name)
                except ModuleNotFoundError as e:
                    print(f"Module {module_name} not found: {e}")
                    continue

                # Iterate through the module and instantiate card classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Card) and attr != Card:
                        card_instance = attr()
                        register_card(card_instance)

                        # Register abilities if the card has them
                        if hasattr(card_instance, 'abilities'):
                            for ability in card_instance.abilities:
                                #Can instantiate them either as classes that require inputs or objects that do not.
                                ability_instance = ability() if isinstance(ability, type) else ability
                                print(f"Instantiating ability: {ability_instance}")
                                register_ability(ability_instance)

                print(f"Done processing card file: {filename}")
                
def DefineSettings():
    #Get Sizes for library, attachments, max battlefield card count, exile zones, graveyards, etc.
    MaxHandSize = obtainpositiveinteger("Input maximum hand size: ")
    MaxLibrarySize = obtainpositiveinteger("Input maximum library size: ")
    MaxGraveyardSize = obtainpositiveinteger("Input maximum graveyard size: ")
    MaxExileZoneSize = obtainpositiveinteger("Input maximum exile zone size: ")
    MaxBattlefieldSize = obtainpositiveinteger("Input maximum battlefield size: ")
    MaxAttachments = obtainpositiveinteger("Input Maximum attachments: ")
    PlayerCount = obtainpositiveinteger("Input number of players: ")
            
    gameSettings = {
        "MaxHandSize":MaxHandSize, 
        "MaxLibrarySize":MaxLibrarySize, 
        "MaxGraveyardSize":MaxGraveyardSize, 
        "MaxExileZoneSize":MaxExileZoneSize,
        "MaxBattlefieldSize":MaxBattlefieldSize,
        "MaxAttachments":MaxAttachments,
        "PlayerCount":PlayerCount
        }
    
    return gameSettings    

def PutCardOntoBattlefield(player, card):
    try:
        #player.Battlefield[0, :] == 0 is a boolean array of the first row (card IDs) of the battlefield. True when a card slot does not contain a card
        #argmax my beloved will scan through this array and output the index of the first occurence of true, in this case
        Index = np.argmax(player.Battlefield[0, :] == 0)
    except:
        raise OverflowError(f"No space in {player}'s Battlefield")
        
    # If all card slots are full, np.argmax returns 0, which could be incorrect.
    if player.Battlefield[0, Index] != 0:
        raise OverflowError(f"No space in {player}'s Battlefield")
    
    player.Battlefield[:, Index] = card

def RemoveCardFromBattlefield(player, TargetCardID, Index):
    if TargetCardID != None:
        # Find the column index of the TargetCardID
        Index = np.argmax(player.Battlefield[0, :] == TargetCardID)
        
        # Check if the card exists in the battlefield
        if player.Battlefield[0, Index] != TargetCardID:
            raise ValueError(f"Card ID {TargetCardID} not found in battlefield.")
        
    elif Index != None:
        #Check if the index is valid
        if Index > player.Battlefield.shape[1] or Index < 0:
            raise ValueError(f"Target index {Index} is not within the battlefield bounds.")
    else:
    
        raise ValueError("No Index or CardID given.")


    # Shift all columns left from the target index
    player.Battlefield[:, Index:-1] = player.Battlefield[:, Index+1:]
    
    # Reset the last column to zero
    player.Battlefield[:, -1] = 0
        

def draw_cards(player, num_cards):
    # Check if the player has enough cards in the library
    if np.count_nonzero(player.Library) < num_cards:
        print(player.Name + " lost the game")
        return  # Exit the function
    
    # Draw the specified number of cards
    for _ in range(num_cards):
        # Get the top card ID
        DrawnCardID = player.Library[0]
        
        # Shift the library and fill the last position with 0
        player.Library[:-1] = player.Library[1:]
        player.Library[-1] = 0
        
        # Check if there's space in the hand
        if not np.any(player.Hand == 0):
            raise OverflowError(f"No space in {player.Name}'s Hand")
        
        # Find the first empty spot in the hand
        HandIndex = np.argmax(player.Hand == 0)
        
        # Place the drawn card into the hand
        player.Hand[HandIndex] = DrawnCardID

def AddCardToExileZone(player, CardID):
    try:
        #player.ExileZone[0, :] == 0 is a boolean array of the first row (card IDs) of the battlefield. True when a card slot does not contain a card
        #argmax my beloved will scan through this array and output the index of the first occurence of true, in this case
        Index = np.argmax(player.ExileZone[0, :] == 0)
    except:
        raise OverflowError(f"No space in {player}'s ExileZone")
        
    # If all card slots are full, np.argmax returns 0, which could be incorrect.
    if player.ExileZone[0, Index] != 0:
        raise OverflowError(f"No space in {player}'s ExileZone")
    
    player.ExileZone[Index] = CardID

def AddCardToGraveyard(player, CardID):
    try:
        #player.Graveyard[0, :] == 0 is a boolean array of the first row (card IDs) of the battlefield. True when a card slot does not contain a card
        #argmax my beloved will scan through this array and output the index of the first occurence of true, in this case
        Index = np.argmax(player.Graveyard[0, :] == 0)
    except:
        raise OverflowError(f"No space in {player}'s Graveyard")
        
    # If all card slots are full, np.argmax returns 0, which could be incorrect.
    if player.Graveyard[0, Index] != 0:
        raise OverflowError(f"No space in {player}'s Graveyard")
    
    player.Graveyard[Index] = CardID

def sacrifice(player, CardID, Index):
    if CardID != None:
        # Find the column index of the TargetCardID
        Index = np.argmax(player.Battlefield[0, :] == CardID)
        
        # Check if the card exists in the battlefield
        if player.Battlefield[0, Index] != CardID:
            raise ValueError(f"Card ID {CardID} not found in battlefield.")
        
    elif Index != None:
        #Check if the index is valid
        if Index > player.Battlefield.shape[1] or Index < 0:
            raise ValueError(f"Target index {Index} is not within the battlefield bounds.")
        else:
            CardID = player.Battlefield[:, Index]
    else:
    
        raise ValueError("No Index or CardID given.")
    
    
    #Removing Card By Index is Faster
    RemoveCardFromBattlefield(player, None, Index)
    AddCardToExileZone(player, CardID)
                
def destroy(player, CardID, Index):
    if CardID != None:
        # Find the column index of the TargetCardID
        Index = np.argmax(player.Battlefield[0, :] == CardID)
        
        # Check if the card exists in the battlefield
        if player.Battlefield[0, Index] != CardID:
            raise ValueError(f"Card ID {CardID} not found in battlefield.")
        
    elif Index != None:
        #Check if the index is valid
        if Index > player.Battlefield.shape[1] or Index < 0:
            raise ValueError(f"Target index {Index} is not within the battlefield bounds.")
        else:
            CardID = player.Battlefield[:, Index]
    else:
    
        raise ValueError("No Index or CardID given.")
    
    RemoveCardFromBattlefield(player, None, Index)
    AddCardToGraveyard(player, CardID)
    
#Untap Step
# - Active Player's Phased in Permanents with phasing controlled by active player phase out.
#   Active Players phased out permanents that the active player controls phases in
# - Phased Out Permanents phase in
# - Active Player's Permanents untap unless a card explicity states otherwise    
    
#Upkeep
# - Active Player Chooses Order of "At the Start of Upkeep" Ability Activation
# - Non-Active Player Chooses Order of "At the Start of Upkeep" Ability Activation
# - I'
#
#
#
#
#
#