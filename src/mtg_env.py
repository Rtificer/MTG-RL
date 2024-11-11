import random
import numpy as np
import CardBase as cb
import AbilityBase as ab
from RegisterCardsAndAbilities import register_all_cards_and_abilities
from Functions import draw_cards
register_all_cards_and_abilities()



class GameState:
    def __init__(self):
        # Define Player Specific Gamestate
        self.CurrentTurn = np.uint8(0)
        #0 for setup and 1-12 for each phase and subphase
        self.GamePhase = np.uint8(20)
        self.Angel = Player("Angel")
        self.Jeremy = Player("Jeremy")
        
class Player:
    def __init__(self, name):
        
        self.Name = name
        self.Life = np.uint8(20)
        self.ManaPool = np.array([0] * 7, dtype = np.uint8) #White, Blue, Black, Red, Green, White, Colorless
        self.Hand = np.array([0] * 0, dtype = np.uint8)
        self.Library = np.array([0] * 30, dtype = np.uint8)
        self.Graveyard = np.array([0] * 0, dtype = np.uint8)
        self.ExileZone = np.array([0] * 0, dtype = np.uint8)
        #Card ID
        #Tapped
        #Summoning Sickness
        #Counters
        #Attachment 1
        #Attachment 2
        #Attachment 3
        #Attachment 4
        #Attachment 5
        self.Battlefield = np.zeros((9, 0), dtype=np.uint8)
            

def GameSetup(game_state):
    AngelStartingCards = 7
    JeremyStartingCards = 7
    
    # Determine who goes first
    if random.choice([0, 1]) == 0:
        print("Jeremy chooses who starts.")
        #TODO:Replace this random.choice for RL Model Ouput on going first or second
        if random.choice([0, 1]) == 0:
            print("Jeremy goes first")
            StartingPlayer = game_state.Jeremy
            SecondPlayer = game_state.Angel
        else:
            print("Angel goes first")
            StartingPlayer = game_state.Angel
            SecondPlayer = game_state.Jeremy
    else:
        print("Angel chooses who starts.")
        #TODO:Replace this random.choice for RL Model Ouput on going first or second
        if random.choice([0, 1]) == 0:
            print("Angel goes first")
            StartingPlayer = game_state.Angel
            SecondPlayer = game_state.Jeremy
        else:
            print("Jeremy goes first")
            StartingPlayer = game_state.Jeremy
            SecondPlayer = game_state.Angel
    
    game_state.Angel.Library = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], dtype = np.uint8)
    np.random.shuffle(game_state.Angel.Library)
    draw_cards(game_state.Angel, AngelStartingCards)
    game_state.Jeremy.Library = np.array([31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60], dtype = np.uint8)
    np.random.shuffle(game_state.Jeremy.Library)
    draw_cards(game_state.Jeremy, JeremyStartingCards)
    
    #Draw starting cards (2 instead of one since you already draw your starting hand)
    while AngelStartingCards >= 2:
        #TODO: Make the RL Model give input on wether or not they want to mulligan, instead of just using RNG.
        if random.choice([0, 1]) == 0:
            break
        else:
            #Reset + Shuffle Angel Library
            game_state.Angel.Hand = np.array([0] * 0, dtype = np.uint8)
            game_state.Angel.Library = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], dtype = np.uint8)
            np.random.shuffle(game_state.Angel.Library)
            draw_cards(game_state.Angel, AngelStartingCards)
            AngelStartingCards += -1
    while JeremyStartingCards >= 2:
        #TODO: Make the RL Model give input on wether or not they want to mulligan, instead of just using RNG.
        if random.choice([0, 1]) == 0:
            break
        else:
            #Reset + Shuffle Jeremy Library
            game_state.Jeremy.Hand = np.array([0] * 0, dtype = np.uint8)
            game_state.Jeremy.Library = np.array([31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60], dtype = np.uint8)
            np.random.shuffle(game_state.Jeremy.Library)
            draw_cards(game_state.Jeremy, JeremyStartingCards)
            JeremyStartingCards += -1
            
    game_state.CurrentTurn += 1
    
    GameRuntime(game_state, StartingPlayer, SecondPlayer)

def GameRuntime(game_state, StartingPlayer, SecondPlayer):
    if game_state.CurrentTurn > 1:
        ActivePlayer = SecondPlayer
        print("Not the First Turn")
        #Untap Subphase (1a)
        #Starts at zero because 1 = Tapped Status
        SecondPlayer.Battlefield[1] = 0
        game_state.GamePhase = 2
        #Upkeep Subphase (1b)
        for CardID in ActivePlayer.Battlefield[0]:
            CardInstance = cb.get_card_by_id(CardID)
            for ability in CardInstance.abilities:
                if ability.trigger == 'upkeep': #check for things that trigger at the begining of the upkeep subphase
                    print(f"Activating {ability.trigger} for card ID {CardID}")
                    ability.activate()
                    
        #TODO: Pack Gamestate
        #TODO: Make the RL Models decide if they wants to cast instants or activate abilities
        
        game_state.GamePhase = 3
        #Draw Subphase (1c)
        draw_cards(SecondPlayer, 1)
        
        #TODO: Pack Gamestate
        #TODO: Make the RL Models decide if they wants to cast instants or activate abilities
        
        game_state.GamePhase = 4
        #Main Phase (2)
        #TODO: Make the RL Model responsible for ActivePlayer decide if it wants to play sorceries, instants, creatures, artifacts, enchantments,  and planeswalkers, and activate abilities. They can play 1 land during this phase
        #TODO: Make the RL Model responsible for the other Player decide if it wants to cast instants or activate the abilities
        #Skip Begining of Combat Subphase bc it's unnessasary
        game_state.GamePhase = 6
        #Declare Attackers Subphase (2b)
    
    else:
        ActivePlayer = StartingPlayer
        game_state.GamePhase = 2
        #Upkeep Subphase (1b)
        for CardID in ActivePlayer.Battlefield[0]:
            CardInstance = cb.get_card_by_id(CardID)
            for ability in CardInstance.abilities:
                if ability.trigger == 'upkeep': #check for things that trigger at the begining of the upkeep subphase
                    print(f"Activating {ability.trigger} for card ID {CardID}")
                    ability.activate()
                    
        #TODO: Pack Gamestate
        #TODO: Make the RL Models decide if they wants to cast instants or activate abilities
        
        #Skip Draw Subphase on first turn
        game_state.GamePhase = 4
        #Main Phase (2)
        #TODO: Make the RL Model responsible for ActivePlayer decide if it wants to play sorceries, instants, creatures, artifacts, enchantments,  and planeswalkers, and activate abilities. They can play 1 land during this phase
        #TODO: Make the RL Model responsible for the other Player decide if it wants to cast instants or activate the abilities
        #Skip Begining of Combat Subphase bc it's unnessasary
        game_state.GamePhase = 6
        #Declare Attackers Subphase (2b)
        for CardID in ActivePlayer.Battlefield[0]:
            CardInstance = cb.get_card_by_id(CardID)
            if "Creature" in CardInstance.types and random.choice([0, 1]) == 0: #Randomness is placeholder for RL decision.
                #TODO: Mark Attacking Creatures as attacking and let the opponent mark defending creatures as defending but defending hard sadge
# Create the game state
game_state = GameState()

# Set up the game and see the output
GameSetup(game_state)
