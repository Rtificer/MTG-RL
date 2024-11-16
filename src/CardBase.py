class Card:
    #cost:  #1=White, 2=Blue, 3=Black, 4=Red, 5=Green, 6=White, 7=Colorless, 8=AnyColor Use o for or, ie. 1o2 means white or blue.
    def __init__(self, card_id, cost = {}, types={}, colors={}, power = None, toughness = None, abilities={}):
        self.card_id = card_id
        self.cost = cost
        self.types = types  #types: Sorcery, Instant, Enchantment, Artifact, Creature, PlanesWalker, Land, BasicLand
        self.colors = colors #1=White, 2=Blue, 3=Black, 4=Red, 5=Green, 6=White, 7=Colorless
        self.power = power
        self.toughness = toughness
        self.abilities = abilities  # List of ability functions or triggers

  
        
CARD_REGISTRY = {}

def register_card(card_instance):
    """Registers a card instance in the CARD_REGISTRY using its card_id."""
    if card_instance.card_id not in CARD_REGISTRY:
        CARD_REGISTRY[card_instance.card_id] = card_instance

def get_card_by_id(card_id):
    """Retrieves a card instance by its ID."""
    return CARD_REGISTRY.get(card_id, None)