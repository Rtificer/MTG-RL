import numpy as np

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