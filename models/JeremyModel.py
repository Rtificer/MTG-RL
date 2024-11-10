import torch
JeremyHandSize = 7
AngelHandSize = 7
JeremyBattlefieldSize = 0
AngelBattlefieldSize = 0
JeremyGraveyardSize = 0
AngelGraveyardSize = 0
JeremyExileZoneSize = 0
AngelExileZoneSize = 0

JeremyLife = torch.tensor(20, dtype = torch.uint8)
AngelLife = torch.tensor(20, dtype = torch.uint8)
#[0]*5 creates a 1 dimensional array with 5 thingies in it, (unsigned 8-bit integers in this case), all set to 0
JeremyManaPool = torch.tensor([0] * 6, dtype = torch.uint8)
AngelManaPool = torch.tensor([0] * 6, dtype = torch.uint8)
#Some Value Much To High To Ever Reach
JeremyHand = torch.tensor([0] * JeremyHandSize, dtype=torch.uint8)
AngelHandSizeTensor = torch.tensor(AngelHandSize, dtype=torch.uint8)
#Card ID
#Tapped
#Summoning Sickness
#Counters
#Attachment 1
#Attachment 2
#Attachment 3
#Attachment 4
#Attachment 5
JeremyBattlefield = torch.zeros((JeremyBattlefieldSize, 9), dtype = torch.uint8)
AngelBattlefield = torch.zeros((AngelBattlefieldSize, 9), dtype = torch.uint8)
JeremyGraveyard = torch.tensor([0] * JeremyGraveyardSize, dtype = torch.uint8)
AngelGraveyard = torch.tensor([0] * AngelGraveyardSize, dtype = torch.uint8)
JeremyExileZone = torch.tensor([0] * JeremyExileZoneSize, dtype = torch.uint8)
AngelExileZone = torch.tensor([0] * AngelExileZoneSize, dtype = torch.uint8)
ActivePlayer = torch.tensor(0, dtype = torch.bool)
AngelLibrarySize = torch.tensor(60, dtype = torch.uint8)
print(ActivePlayer)