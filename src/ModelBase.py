import torch
import torch.nn as nn
import torch.optim as optim
from mtg_env import gameSettings

class MTGRLModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(MTGRLModel, self).__init__()
        self.input = nn.Linear(input_size, 128)
        self.hidden1 = nn.Linear(128, 128)
        self.hidden2 = nn.Linear(128, 128)
        self.hidden3 = nn.Linear(128, 128)
        self.hidden4 = nn.Linear(128, 64)
        self.output = nn.Linear(64, output_size)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x):
        x = self.relu(self.input(x))
        x = self.relu(self.hidden1(x))
        x = self.softmax(self.output(x))
        return x

# Example initialization
input_size = 100  # Adjust based on your game state encoding
output_size = 20  # Adjust based on maximum number of attacking creatures
rl_model = MTGRLModel(input_size, output_size)