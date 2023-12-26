import math

# playerCount = 5
# potForOpt = {}
# playerOptSelection = {}
# playerPointsBet = {}

def distrPoints(playerOptSelection, potForOpt, betPoints, winOption):
    result = {}
    n = 0
    for value in playerOptSelection.values():
        if value == winOption:
            n = n + 1
    
    sumAmount = 0
    for pot, amount in potForOpt.items():
        if pot == -1: 
            continue

        if pot != winOption:
            sumAmount = sumAmount + amount

    if n == 0:
        n = 1

    indPayout = int(math.ceil(sumAmount/n))
    if indPayout <= 0:
        indPayout = 1

    for key, value in playerOptSelection.items():
        if value == -1:
            result[key] = 0
            continue

        if value != winOption:
            result[key] = -betPoints
            print(f"Player {key} looses {betPoints} Points")
            continue
        # payoutPlayer = indPayout + playerPointsBet[key]
        result[key] = indPayout + betPoints
        print(f"Player {key} gets {indPayout} Points")

    return result


"""
while True:
    for i in range(playerCount):
        playerOptSelection[i] = int(input(f"Select Option for Player {i}: "))
        playerPointsBet[i] = int(input(f"How many Points does Player {i} bet: "))

    for value in playerOptSelection.values():
        potForOpt[value] = 0
    
    for key, value in playerOptSelection.items():
        potForOpt[value] = potForOpt[value] + playerPointsBet[key]


    selOption = int(input("Which Option Won: "))

    distrPoints(selOption)

"""