                RemainingPower = CardInstance.power
                CurrentDefender = 1
                while CurrentDefender <= DefendersQuantity:
                    ActivePlayer.Battlefield[4, CardIndex] -= InactivePlayer.Battlefield[5, DefenderIndexes[CurrentDefender - 1]]
                    InactivePlayer.Battlefield[4, ]
                    CurrentDefender += 1
                else:
                    InactivePlayer.Life -= RemainingPower