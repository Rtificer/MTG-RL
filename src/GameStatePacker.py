import torch
import numpy as np

def PackGameState(game_state, gameSettings):
    """
    Packs the game state from the perspective of every player.
    Args:
        game_state: The current game state.
        gameSettings: The game settings.

    Returns:
        torch.Tensor: A packed tensor containing all players' perspectives of the game state.
    """
    all_player_views = []

    for player in game_state.Players:  # The player whose perspective we're encoding
        
        
        
        
        
        
        
        player_view = []
        for observed_player in game_state.Players:  # The player being observed
            if observed_player.ID == player.ID:  # Full view for the observing player
                player_view.append(
                    torch.cat((
                        torch.tensor([observed_player.Life], dtype=torch.float32),
                        torch.tensor(observed_player.ManaPool, dtype=torch.float32),
                        torch.tensor(observed_player.Hand, dtype=torch.float32),
                        torch.tensor(observed_player.Graveyard, dtype=torch.float32),
                        torch.tensor(observed_player.ExileZone, dtype=torch.float32),
                        torch.tensor(observed_player.Battlefield.flatten(), dtype=torch.float32),
                    ))
                )
            else:  # Limited view for other players
                player_view.append(
                    torch.cat((
                        torch.tensor([observed_player.Life], dtype=torch.float32),
                        torch.tensor(observed_player.ManaPool, dtype=torch.float32),
                        torch.tensor(observed_player.Graveyard, dtype=torch.float32),
                        torch.tensor(observed_player.ExileZone, dtype=torch.float32),
                        torch.tensor(observed_player.Battlefield.flatten(), dtype=torch.float32),
                    ))
                )

        # Combine all observed players' views for this player's perspective
        all_player_views.append(torch.cat(player_view))

    # Stack all players' views into a single tensor
    return torch.stack(all_player_views)