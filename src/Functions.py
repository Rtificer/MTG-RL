import numpy as np
import sys
import os
import importlib
from CardBase import Card, register_card
from AbilityBase import register_ability
from DeckBase import Deck

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
    # Add Decks path to sys.path
    decks_path = os.path.join(os.getcwd(), "Assets", "Decks")
    sys.path.append(decks_path)

    Decks = os.listdir(decks_path)
    for deck in Decks:
        print(f"Deck: {deck}")

        # Import DeckAttributes.py
        deck_attributes_path = os.path.join(decks_path, deck, "DeckAttributes.py")
        if os.path.isfile(deck_attributes_path):
            module_name = f"{deck}.DeckAttributes"
            try:
                module = importlib.import_module(module_name)
                # Find the Deck class and instantiate it
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Deck) and attr != Deck:
                        deck_instance = attr()
                        print(f"Loaded deck attributes: {deck_instance}")
                        break
            except ModuleNotFoundError as e:
                print(f"Module {module_name} not found: {e}")
                continue

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