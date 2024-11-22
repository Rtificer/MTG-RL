import numpy as np
import sys
import os
import importlib
from CardBase import Card, register_card
from AbilityBase import register_ability
from DeckBase import Deck

def register_decks():
    # Add Decks directory to sys.path
    decks_path = os.path.join(os.getcwd(), "Assets", "Decks")
    sys.path.append(decks_path)

    deck_library_lists = {}

    Decks = os.listdir(decks_path)
    for deck in Decks:
        print(f"Processing deck: {deck}")
        
        deck_module_name = f"{deck}.DeckAttributes"
        
        try:
            # Import the deck module and extract the library list
            deck_module = importlib.import_module(deck_module_name)
            deck_instance = deck_module.Deck()  # Create an instance of the Deck class
            librarylist = deck_instance.librarylist
            deck_library_lists[deck] = librarylist
            print(f"Library list for {deck}: {librarylist}")
        
        except ModuleNotFoundError as e:
            print(f"Module {deck_module_name} not found: {e}")
            continue
    
    return deck_library_lists

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
                                ability_instance = ability() if isinstance(ability, type) else ability
                                print(f"Instantiating ability: {ability_instance}")
                                register_ability(ability_instance)

                print(f"Done processing card file: {filename}")
                
def DefineSettings():
    #Get Sizes for library, attachments, max battlefield card count, exile zones, graveyards, etc.
    while True:
        
        MaxHandSize = input("Input maximum hand size:")
        if isinstance(MaxHandSize, int) and MaxHandSize > 0: 
            break
        else:
            print(f"{MaxHandSize} is not a valid maximum hand size.")    
    
    while True:
        
        MaxLibrarySize = input("Input maximum library size:")
        if isinstance(MaxLibrarySize, int) and MaxLibrarySize > 0: 
            break
        else:
            print(f"{MaxLibrarySize} is not a valid maximum library size.")
            
    while True:
        
        MaxGraveyardSize = input("Input maximum graveyard size:")
        if isinstance(MaxGraveyardSize, int) and MaxGraveyardSize > 0: 
            break
        else:
            print(f"{MaxGraveyardSize} is not a valid maximum graveyard size.")
            
    while True:
        
        MaxExileZoneSize = input("Input maximum exile zone size:")
        if isinstance(MaxExileZoneSize, int) and MaxExileZoneSize > 0: 
            break
        else:
            print(f"{MaxExileZoneSize} is not a valid maximum exile zone size.")
            
    while True:
        
        MaxBattlefieldSize = input("Input maximum battlefield size:")
        if isinstance(MaxBattlefieldSize, int) and MaxBattlefieldSize > 0: 
            break
        else:
            print(f"{MaxBattlefieldSize} is not a valid battlefield library size.")

    while True:
        MaxAttachments = input("Input Maximum attachments:")
        if isinstance(MaxAttachments, int) and MaxAttachments > 0: 
            break
        else:
            print(f"{MaxAttachments} is not a valid number of maximum attachments.")
            
    gameSettings = {
        "MaxHandSize":MaxHandSize, 
        "MaxLibrarySize":MaxLibrarySize, 
        "MaxGraveyardSize":MaxGraveyardSize, 
        "MaxExileZoneSize":MaxExileZoneSize,
        "MaxBattlefieldSize":MaxBattlefieldSize,
        "MaxAttachments":MaxAttachments
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
    if player.Library.size < num_cards:
        print(player.Name + " lost the game")
    else:
        # Draw the specified number of cards
        for _ in range(num_cards):
            player.Hand = np.append(player.Hand, player.Library[0])
            player.Libary = np.delete(player.Library, 0)
        print(f"Player {player.Name} has drawn {num_cards} cards.")
        print("New hand: " + str(player.Hand))
        print("Updated library: " + str(player.Library))

def sacrifice(targetplayer, target):
    for CardIndex in range(targetplayer.Battlefield.shape[0]):
        CardID = targetplayer.Battlefield[0, CardIndex]
        if CardID == target:
            targetplayer.ExileZone = np.append(targetplayer.ExileZone, CardID)
            targetplayer.Battlefield = np.delete(targetplayer.Battlefield, CardIndex, axis = 1)
            
def destroy(targetplayer, target):
    for CardIndex in range(targetplayer.Battlefield.shape[0]):
        CardID = targetplayer.Battlefield[0, CardIndex]
        if CardID == target:
            targetplayer.Graveyard = np.append(targetplayer.Graveyard, CardID)
            targetplayer.Battlefield = np.delete(targetplayer.Battlefield, CardIndex, axis = 1)