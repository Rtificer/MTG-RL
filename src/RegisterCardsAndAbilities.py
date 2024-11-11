import os
import importlib
from CardBase import register_card
from AbilityBase import register_ability

def register_all_cards_and_abilities():
    card_folder = '../../Assets/Cards'
    # Iterate through each file in the specified folder
    for filename in os.listdir(card_folder):
        # Check if the file is a Python file and is not the __init__.py file
        if filename.endswith('.py'):
            # Construct the module name for import (e.g., 'Cards.Wastes')
            module_name = f"{card_folder}.{filename[:-3]}"
            
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
            
register_all_cards_and_abilities()