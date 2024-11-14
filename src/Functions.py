import numpy as np
import os
import importlib
from CardBase import register_card
from AbilityBase import register_ability

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

def register_decks():
    Assets = os.listdir("./Assets/Decks")
    for deck in Assets:
        print(deck)
        print(os.listdir(f"./Assets/Decks/{deck}/Cards"))
        for filename in os.listdir(deck):
            # Construct the module name for import (e.g., 'Cards.Wastes')
            module_name = f"{deck}.{filename[:-3]}"
            print(module_name)
            # Import the module dynamically
            module = importlib.import_module(module_name)
            
            # Iterate over all attributes in the imported module
            for attr_name in dir(module):
                # Get the attribute (class, function, variable, etc.) by name
                attr = getattr(module, attr_name)
                
                # Create an instance of the card class
                card_instance = attr()
                
                # Register the card instance in the CARD_REGISTRY
                register_card(card_instance)
                
                for ability in card_instance.abilities:
                    register_ability(ability)

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