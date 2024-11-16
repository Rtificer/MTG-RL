class Ability:
    def __init__(self, ability_id, trigger, effect):
        self.trigger = trigger  # When to trigger, e.g., 'upkeep'
        self.effect = effect    # Effect function to execute
        self.ability_id = ability_id

    def activate(self, targetplayers = [], TargetCardID = []):
        self.effect(targetplayers, TargetCardID)


ABILITY_REGISTRY = {}

def register_ability(ability_instance):
    """Registers an ability instance in the ABILITY_REGISTRY using its trigger or ID."""
    if ability_instance.ability_id not in ABILITY_REGISTRY:
        ABILITY_REGISTRY[ability_instance.ability_id] = ability_instance

def get_ability_by_id(ability_id):
    """Retrieves an ability instance by its trigger."""
    return ABILITY_REGISTRY.get(ability_id, None)