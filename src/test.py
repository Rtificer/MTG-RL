import sys
import os
import importlib
from CardBase import Card, register_card  # Import Card class
from AbilityBase import register_ability

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
                    card_instance = attr()  # This should now instantiate the correct card class
                    register_card(card_instance)

                    # Register abilities if the card has them
                    if hasattr(card_instance, 'abilities'):
                        for ability in card_instance.abilities:
                            # Ensure abilities are instantiated before registering
                            ability_instance = ability()
                            print(f"Instantiating ability: {ability_instance}")
                            register_ability(ability_instance)
            
            print(f"Done processing card file: {filename}")