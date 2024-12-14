import random
import numpy as np
import CardBase as cb
import AbilityBase as ab
from Functions import draw_cards
from Functions import register_decks
from Functions import register_cards
from Functions import DefineSettings
from utils.utilities import StartIndexArray
from utils.utilities import TwoDimensionalStartIndexArray


register_cards()
gameSettings = DefineSettings()
deck_data = register_decks()


class GameState:
    def __init__(self):
        # Define Player Specific Gamestate
        self.CurrentTurn = np.uint8(0)
        #0 for setup and 1-12 for each phase and subphase
        self.GamePhase = np.uint8(20)
        self.Players = []
        self.TurnOrder = []
        
class Player:
    
    
    def __init__(self, name, ID, gameSettings):
        
        self.Name = name
        self.ID = ID
        
        self.Perspective = PlayerPerspective(self.ID, gameSettings, deck_data)
        
        self.Deck = None
        self.Life = np.uint8(20)
        self.ManaPool = StartIndexArray(6) #White, Blue, Black, Red, Green, Colorless
        self.Hand = StartIndexArray(gameSettings["MaxHandSize"])
        self.Library = StartIndexArray(gameSettings["MaxLibrarySize"])
        self.Graveyard = StartIndexArray(gameSettings["MaxGraveyardSize"])
        self.ExileZone = StartIndexArray(gameSettings["MaxExileZoneSize"])
        #Card ID
        #Tappedy
        #Summoning Sickness
        #Counters
        #Remaining Toughness
        #Current Attack
        #Attachments
        self.Battlefield = TwoDimensionalStartIndexArray(6 + gameSettings["MaxAttachments"], gameSettings["MaxBattlefieldSize"])
        
class PlayerPerspective:
    
    def __init__(self, playerID, gameSettings, deck_data):
        #Dictionary Holding Persepctive Data
        self.Data = {}
        
        
        for player in game_state.Players:
            if player.ID == playerID:
                #Persepctive of this player
                
                totalcardcount = deck_data[player.Deck]["TotalCardCount"]                
                
                self.Data[playerID] = {
                    "DefaultProbabilityVector" : np.zeros(totalcardcount, dtype = np.uint16),
                    "AdditonalVectors" : []
                    
                }
                
            else:
                
                totalcardcount = deck_data[player.Deck]["TotalCardCount"]
                
                self.Data[player.ID] = {
                    
                    "DefaultProbabilityVector" : np.zeros(totalcardcount, dtype = np.uint16),
                    "AdditonalVectors" : []
                    
                }            
        
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

def GameSetup(game_state, StartingLibraries):

    #Shuffle Player Libraries
    for player in game_state.Players:
        np.random.shuffle(player.Library)

            

    
    # Determine who goes first
    StartChooser = random.choice(game_state.Players)
    #TODO: Make the RL Model give input on who the startchooser decides goes first instead of just doing another random.choice
    StartingPlayer = random.choice(game_state.Players)
    
    #Establish Turn Order
    for Player in game_state.Players:
        if Player != StartingPlayer:
            game_state.TurnOrder.append(Player)
            
    random.shuffle(game_state.TurnOrder)
    
    game_state.TurnOrder.insert(0, StartingPlayer)

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
    if game_state.CurrentTurn < 1:
        ActivePlayer = StartingPlayer
        ActivePlayerIndex = 0
        print("First turn not implemented yet")
    else:
        if ActivePlayerIndex < len(game_state.TurnOrder):
            ActivePlayerIndex += 1
        else:
            ActivePlayerIndex = 0
        print("Not the First Turn")
        #Untap Subphase (1a)
        #Starts at zero because 1 = Tapped Status
        ActivePlayer.Battlefield[1] = 0
        game_state.GamePhase = 2
        #Upkeep Subphase (1b)
        #Creates a boolean array that is true when the first value in each column is not zero, and false otherwise. Than uses this mask to mask the first row the battlefield, returning the card ID's of all cards in the battlefield.
        OccupiedBattlefieldSlotsCardIDs = ActivePlayer.Battlefield[0, ActivePlayer.Battlefield[0, :] != 0]
        
        for CardID in OccupiedBattlefieldSlotsCardIDs:
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
        #TODO: Make the RL Model responsible for the other Players decide if they wants to cast instants or activate the abilities
        #Skip Begining of Combat Subphase bc it's unnessasary
        game_state.GamePhase = 6
        #Declare Attackers Subphase (2b)
        
        OccupiedBattlefieldSlotsMask = ActivePlayer.Battlefield[0, :] != 0
        for CardIndex in np.where(OccupiedBattlefieldSlotsMask)[0]:
            if ActivePlayer.Battlefield[1, CardIndex] == 0 and ActivePlayer.Battlefield[2, CardIndex] == 0:   #Start by only checking the thing that doesn't require indexing the Card registry
                CardInstance = cb.get_card_by_id(CardIndex[0])
                #If the card is a creature that isn't tapped and does not have summoning sickness
                if "Creature" in CardInstance.types:
                    #TODO: Mark That Card As Attacking
                    return
                    
        game_state.GamePhase = 7
        #Declare Defenders Subphase (2c)

            
                    
                    
                    

# Create the game state
game_state = GameState()

# Set up the game and see the output
GameSetup(game_state)
