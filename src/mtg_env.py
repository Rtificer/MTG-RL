import random
import numpy as np
import CardBase as cb
import AbilityBase as ab
from Functions import draw_cards
from Functions import register_decks
from Functions import register_cards
register_cards()
register_decks()



class GameState:
    def __init__(self):
        # Define Player Specific Gamestate
        self.CurrentTurn = np.uint8(0)
        #0 for setup and 1-12 for each phase and subphase
        self.GamePhase = np.uint8(20)
        self.Players = []
        
class Player:
    def __init__(self, name):
        
        self.Name = name
        self.Deck = None
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
        #Remaining Toughness
        #Current Attack
        #Attacking?
        #Defender 1
        #Defender 2
        #Defender 3
        #Defender 4
        #Defender 5
        #Defender 6
        #Defender 7
        #Defender 8
        #Attachment 1
        #Attachment 2
        #Attachment 3
        #Attachment 4
        #Attachment 5
        self.Battlefield = np.zeros((19, 0), dtype=np.uint8)
        

def GameSetup(game_state):
    #Get the starting libraries associated with each deck
    StartingLibraries = register_decks()
    while True:
        #Get the Number of Players
        numplayers = input("Input Number of Players")
        if isinstance(numplayers, int) and numplayers > 0:
            i = 0
            while i < numplayers:
                
                PlayerName = input(f"Input Player{i} Name")
                game_state.Players.append(Player(PlayerName))
                #Get the Deck for each player
                while True (PlayerName):
                    PlayerDeck = input(f"Input Deck For {PlayerName}")
                    if PlayerDeck in StartingLibraries:
                        #Add that deck as the player's deck.
                        game_state.Players[i].Deck = PlayerDeck
                        #Add That Deck to the Players Library
                        game_state.Players[i].Library = StartingLibraries[PlayerDeck]
                    else:
                        print(f"Deck {PlayerDeck} not found")
                i += 1
            else:
                break
        else:
            print(f"{numplayers} is not a valid playercount")
        #Shuffle Player Libraries
        for Player in game_state.Players:
            np.random.shuffle(Player.Library)
            
    
    AngelStartingCards = 7
    JeremyStartingCards = 7
    
    # Determine who goes first
    StartChooser = random.choice(game_state.Players)
    #TODO: Make the RL Model give input on who the startchooser decides goes first instead of just doing another random.choice
    StartingPlayer = random.choice(game_state.Players)
    

    
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
    
    GameRuntime(game_state, StartingPlayer)

def GameRuntime(game_state, StartingPlayer):
    if game_state.CurrentTurn > 1:
        if ActivePlayer == game_state.Angel:
            ActivePlayer = game_state.Jeremy
            InactivePlayer = game_state.Angel
        else:
            ActivePlayer = game_state.Angel
            InactivePlayer = game_state.Jeremy
        print("Not the First Turn")
        #Untap Subphase (1a)
        #Starts at zero because 1 = Tapped Status
        ActivePlayer.Battlefield[1] = 0
        game_state.GamePhase = 2
        #Upkeep Subphase (1b)
        for CardID in ActivePlayer.Battlefield[0]:
            CardInstance = cb.get_card_by_id(CardID)
            for ability in CardInstance.abilities:
                if ability.trigger == 'upkeep': #check for things that trigger at the begining of the upkeep subphase
                    print(f"Activating {ability.trigger} for card ID {CardID}")
                    ability.activate()
             
        #TODO: Make the RL Models decide if they wants to cast instants or activate abilities
        
        game_state.GamePhase = 3
        #Draw Subphase (1c)
        draw_cards(ActivePlayer, 1)

        #TODO: Make the RL Models decide if they wants to cast instants or activate abilities
        
        game_state.GamePhase = 4
        #Main Phase (2)
        #TODO: Make the RL Model responsible for ActivePlayer decide if it wants to play sorceries, instants, creatures, artifacts, enchantments,  and planeswalkers, and activate abilities. They can play 1 land during this phase
        #TODO: Make the RL Model responsible for the other Player decide if it wants to cast instants or activate the abilities
        #Skip Begining of Combat Subphase bc it's unnessasary
        game_state.GamePhase = 6
        #Declare Attackers Subphase (2b)
        for CardIndex in range(ActivePlayer.Battlefield.shape[0]):
            if ActivePlayer.Battlefield[1, CardIndex] == 0 and ActivePlayer.Battlefield[2, CardIndex] == 0:   #Start by only checking the thing that doesn't require indexing the Card registry
                CardID = ActivePlayer.Battlefield[0, CardIndex]
                CardInstance = cb.get_card_by_id(CardID)
                #If the card is a creature that isn't tapped and does not have summoning sickness
                if "Creature" in CardInstance.types:
                    if random.choice([0, 1]) == 0: #Randomness is placeholder for RL decision. Delete when implemented
                        ActivePlayer.Battlefield[6, CardIndex] = 1 #Mark That Card As Attacking
                    
        game_state.GamePhase = 7
        #Declare Defenders Subphase (2c)
        #For every Card In the Defending players library
        for CardIndex in range(InactivePlayer.Battlefield.shape[0]):
            if ActivePlayer.Battlefield[1, CardIndex] == 0:  #Start by only checking the thing that doesn't require indexing the Card registry
                CardID = InactivePlayer.Battlefield[0, CardIndex]
                CardInstance = cb.get_card_by_id(CardID)
                #If the card is an untapped creature
                if "Creature" in CardInstance.types:
                    #Go through every card in the opponents library
                    for CardIndex in range(ActivePlayer.Battlefield.shape[0]):
                        #If that card is attacking
                        if ActivePlayer.Battlefield[6, CardIndex] == 1:
                            #And the Rl model wants to defend it
                            if random.choice([0, 1]) == 0: #Randomness is placeholder for RL decision. Delete when implemented
                                DefenderSlot = 7 #Would be 8 becuase of the 8 slots, but is 15 bc the defender slots start 8 units down, and 0 is the first index
                                #Iterate through every defender slot on the attacking card
                                while DefenderSlot <= 15:
                                    #Check if it's available
                                    if ActivePlayer.Battlefield[DefenderSlot, CardIndex] == 0:
                                        #If it is mark this card as defending it (in the first available slot)
                                        ActivePlayer.Battlefield[DefenderSlot, CardIndex] = CardID
                                    else:
                                    #If its not available try again on the next one
                                        DefenderSlot += 1
                                else:
                                    print("Error: Ran out of defender slots") 

        #TODO: Make the RL Models decide if they wants to cast instants or activate abilities

    else:
        ActivePlayer = StartingPlayer
        if ActivePlayer == game_state.Angel:
            InactivePlayer = game_state.Angel
        else:
            InactivePlayer = game_state.Jeremy
            
        game_state.GamePhase = 2
        #Upkeep Subphase (1b)
        for CardID in ActivePlayer.Battlefield[0]:
            CardInstance = cb.get_card_by_id(CardID)
            for ability in CardInstance.abilities:
                if ability.trigger == 'upkeep': #check for things that trigger at the begining of the upkeep subphase
                    print(f"Activating {ability.trigger} for card ID {CardID}")
                    ability.activate()
                    
        #TODO: Make the RL Models decide if they wants to cast instants or activate abilities
        
        #Skip Draw Subphase on first turn
        game_state.GamePhase = 4
        #Main Phase (2)
        #TODO: Make the RL Model responsible for ActivePlayer decide if it wants to play sorceries, instants, creatures, artifacts, enchantments,  and planeswalkers, and activate abilities. They can play 1 land during this phase
        #TODO: Make the RL Model responsible for the other Player decide if it wants to cast instants or activate the abilities
        #Skip Begining of Combat Subphase bc it's unnessasary
        game_state.GamePhase = 6
        #Declare Attackers Subphase (2b)
        for CardIndex in range(ActivePlayer.Battlefield.shape[0]):
            if ActivePlayer.Battlefield[1, CardIndex] == 0 and ActivePlayer.Battlefield[2, CardIndex] == 0:   #Start by only checking the thing that doesn't require indexing the Card registry
                CardID = ActivePlayer.Battlefield[0, CardIndex]
                CardInstance = cb.get_card_by_id(CardID)
                #If the card is a creature that isn't tapped and does not have summoning sickness
                if "Creature" in CardInstance.types:
                    if random.choice([0, 1]) == 0: #Randomness is placeholder for RL decision. Delete when implemented
                        ActivePlayer.Battlefield[6, CardIndex] = 1 #Mark That Card As Attacking
                    
        game_state.GamePhase = 7
        #Declare Defenders Subphase (2c)
        #For every Card In the Defending players library
        for CardIndex in range(InactivePlayer.Battlefield.shape[0]):
            if ActivePlayer.Battlefield[1, CardIndex] == 0:  #Start by only checking the thing that doesn't require indexing the Card registry
                CardID = InactivePlayer.Battlefield[0, CardIndex]
                CardInstance = cb.get_card_by_id(CardID)
                #If the card is an untapped creature
                if "Creature" in CardInstance.types:
                    #Go through every card in the opponents library
                    for CardIndex in range(ActivePlayer.Battlefield.shape[0]):
                        #If that card is attacking
                        if ActivePlayer.Battlefield[6, CardIndex] == 1:
                            #And the Rl model wants to defend it
                            if random.choice([0, 1]) == 0: #Randomness is placeholder for RL decision. Delete when implemented
                                DefenderSlot = 7 #Would be 8 becuase of the 8 slots, but is 15 bc the defender slots start 8 units down, and 0 is the first index
                                #Iterate through every defender slot on the attacking card
                                while DefenderSlot <= 15:
                                    #Check if it's available
                                    if ActivePlayer.Battlefield[DefenderSlot, CardIndex] == 0:
                                        #If it is mark this card as defending it (in the first available slot)
                                        ActivePlayer.Battlefield[DefenderSlot, CardIndex] = CardID
                                        break
                                    else:
                                    #If its not available try again on the next one
                                        DefenderSlot += 1
                                else:
                                    print("Error: Ran out of defender slots") 

        #TODO: Make the RL Models decide if they wants to cast instants or activate abilities

        game_state.GamePhase = 8
        #Combat Damage Subphase (2d)
        for CardIndex in range(ActivePlayer.Battlefield.shape[0]):
            if ActivePlayer.Battlefield[6, CardIndex] == 1: #for every creature that is attacking
                CardID = ActivePlayer.Battlefield[0, CardIndex]
                CardInstance = cb.get_card_by_id(CardID)
                #Get the defenders into a list for the purpose of randomization in place of the RL Model
                DefenderIndexes = []
                DefendersChecked = 0
                DefendersQuantity = 0
                #Iterate through every defender slot on the attacking card
                while DefendersChecked <= 8:
                    #Check if theirs a defender
                    if ActivePlayer.Battlefield[DefendersChecked + 7, CardIndex] != 0:
                        #Get their ID
                        DefenderID = ActivePlayer.Battlefield[DefendersChecked + 7, CardIndex]
                        #Get the Index of that defender in the opponents battlefield
                        for DefenderCardIndex in range(InactivePlayer.Battlefield.shape[0]):
                            #If they find that card id
                            if InactivePlayer.Battlefield[0, CardIndex] == DefenderID:
                                #Add that Card ID to a list of defender indexes
                                DefenderIndexes.append(DefenderCardIndex)
                                DefendersQuantity += 1
                    else:
                        break
                random.shuffle(DefenderIndexes)
                #TODO: Replace this randomization and the placing of the defenders into a list with a decision from the RL Model
            
                    
                    
                    

# Create the game state
game_state = GameState()

# Set up the game and see the output
GameSetup(game_state)
