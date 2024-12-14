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