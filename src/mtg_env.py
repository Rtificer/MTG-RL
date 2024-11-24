import random
import numpy as np
import CardBase as cb
import AbilityBase as ab
from Functions import draw_cards
from Functions import register_decks
from Functions import register_cards
from Functions import DefineSettings

register_cards()
gameSettings = DefineSettings()


class GameState:
    def __init__(self):
        # Define Player Specific Gamestate
        self.CurrentTurn = np.uint8(0)
        #0 for setup and 1-12 for each phase and subphase
        self.GamePhase = np.uint8(20)
        self.Players = []
        self.TurnOrder = np.array([0] * gameSettings["PlayerCount"], dtype = np.uint8)
        
class Player:
    
    
    def __init__(self, name, ID, gameSettings):
        
        self.Name = name
        self.ID = ID
        self.Deck = None
        self.Life = np.uint8(20)
        self.ManaPool = np.array([0] * 7, dtype = np.uint8) #White, Blue, Black, Red, Green, White, Colorless
        self.Hand = np.array([0] * gameSettings["MaxHandSize"], dtype = np.uint8)
        self.Library = np.array([0] * gameSettings["MaxLibrarySize"], dtype = np.uint8)
        self.Graveyard = np.array([0] * gameSettings["MaxGraveyardSize"], dtype = np.uint8)
        self.ExileZone = np.array([0] * gameSettings["MaxExileZoneSize"], dtype = np.uint8)
        #Card ID
        #Tapped
        #Summoning Sickness
        #Counters
        #Remaining Toughness
        #Current Attack
        #Attachments
        self.Battlefield = np.zeros((6 + gameSettings["MaxAttachments"], gameSettings["MaxBattlefieldSize"]), dtype=np.uint8)
        
def SetupGameState():
    #Get the starting libraries associated with each deck
    StartingLibraries = register_decks()

    i = 0
    while i < gameSettings["PlayerCount"]:
        PlayerName = input(f"Input Player{i} Name")
        game_state.Players.append(Player(PlayerName, i+1, gameSettings))
        #Get the Deck for each player
        while True (PlayerName):
            PlayerDeck = input(f"Input Deck For {PlayerName}")
            if PlayerDeck in StartingLibraries:
                #Add that deck as the player's deck.
                game_state.Players[i].Deck = PlayerDeck
                #Add That Deck to the Players Library
                game_state.Players[i].Library = StartingLibraries[PlayerDeck]
                break
            else:
                print(f"Deck {PlayerDeck} not found")

        i += 1

def GameSetup(game_state):

    #Shuffle Player Libraries
    for player in game_state.Players:
        np.random.shuffle(player.Library)

            

    
    # Determine who goes first
    StartChooser = random.choice(game_state.Players)
    #TODO: Make the RL Model give input on who the startchooser decides goes first instead of just doing another random.choice
    StartingPlayer = random.choice(game_state.Players)
    
    #Establish Turn Order
    Index = 0
    for Player in game_state.Players:
        if Player != StartingPlayer:
            Index += 1
            game_state.TurnOrder[Index] = Player.ID
            
    np.random.shuffle(game_state.TurnOrder)
    
    game_state.TurnOrder[0] = StartingPlayer.ID

    for Player in game_state.Players:
        draw_cards(Player, 7)
    
    
    #Handle Mulligans
    MulliganingPlayers = []
    RemainingCardDrawCount = 6
    while len(MulliganingPlayers) > 0:
        for Player in game_state.TurnOrder not in MulliganingPlayers:
            #TODO: Make the RL Model give input on wether or not they want to mulligan, instead of just using RNG.
            if random.choice([0, 1]) == 0:
                Player.Library = StartingLibraries[Player.Deck]
                Player.Hand.fill(0)
                draw_cards(Player, RemainingCardDrawCount)
        
        RemainingCardDrawCount -= 1
            
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
