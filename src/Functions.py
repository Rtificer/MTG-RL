import numpy as np
import sys
import os
import importlib
from CardBase import Card, register_card
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
    # Add Decks and Abilities directories to sys.path
    decks_path = os.path.join(os.getcwd(), "Assets", "Decks")
    sys.path.append(decks_path)

    Decks = os.listdir(decks_path)
    for deck in Decks:
        print(f"Deck: {deck}")

        cards_dir = os.path.join(decks_path, deck, "Cards")

        for filename in os.listdir(cards_dir):
            if filename != '__init__.py' and not filename.startswith('__pycache__'):
                print(f"Processing card file: {filename}")
                # Adjust module name for Cards directory
                module_name = f"{deck}.Cards.{filename[:-3]}"

                module = importlib.import_module(module_name)

                #Iterate through the module and look for classes to instantiate
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    # Check if it is a class and if it's the correct class
                    if isinstance(attr, type) and issubclass(attr, Card) and attr != Card:  # Ensures that attr is a class a subclass of Card, and not the Card class itself
                        card_instance = attr()
                        register_card(card_instance)

                        # Register abilities if the card has them
                        if hasattr(card_instance, 'abilities'):
                            for ability in card_instance.abilities:
                                ability_instance = ability()
                                print(f"Instantiating ability: {ability_instance}")
                                register_ability(ability_instance)
                
                print(f"Done processing card file: {filename}")

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