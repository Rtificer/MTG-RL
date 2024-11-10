class Ability:
    def __init__(self, trigger, effect):
        self.trigger = trigger  # When to trigger, e.g., 'upkeep'
        self.effect = effect    # Effect function to execute

    def activate(self, targetplayers = [], TargetCardID = []):
        self.effect(targetplayers, TargetCardID)


ABILITY_REGISTRY = {}

def register_ability(ability_instance):
    """Registers an ability instance in the ABILITY_REGISTRY using its trigger or ID."""
    if ability_instance.trigger not in ABILITY_REGISTRY:
        ABILITY_REGISTRY[ability_instance.trigger] = ability_instance

def get_ability_by_trigger(trigger):
    """Retrieves an ability instance by its trigger."""
    return ABILITY_REGISTRY.get(trigger, None)