from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from Creature import Creature
from Genome import Genome
from Board import Board
import secrets
import random

boardHeight = 100
boardWidth = 100
plt.style.use('seaborn')
initialGenomes = []
initialGenomes.append(Genome("09dfb7788f504bb0a068cb59dbb222e684021f3ee88f74476ddf1028f2831186fce2897d0ebd8"))
initialGenomes.append(Genome("49fd3fe26c103e27628c60497b25889a1f561e838e65ef83e4b9aa85bafda93a93d1694799fbe"))
initialGenomes.append(Genome("a4d98ec24f60fea6d41ac9a37351272f169d2d327cc2afd33dda1a1beefa9217c0d0abdc"))
initialGenomes.append(Genome("68fd3fc07c9008d6555a3c6b59445bd26ae8f6038e8e167b7f96b4a803a1a91274feffca45bd3"))
initialGenomes.append(Genome("0cf676c03c006ea3116d00327920e77c5a066596b0c5c14766e55c03b23e42e4d60043ef0ab88c89ad"))

creatureList = []
for i in range(1000):
    #creatureList.append(Creature(0,Genome(secrets.token_hex(68)),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1),))
    #creatureList.append(Creature(0,Genome("7fec28040b24107708310c007b623ab36562bc895bf006d6238a3ba743930768ea77c624fae4a4eafa42b7167b1867e0d2bcdad7f5eabdcd8ba4e6a009ba83cba8382a83"),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1),))
    #creatureList.append(Creature(random.choice([0,1]),random.choice(initialGenomes),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1)))
    
    if random.choice([False,False,False,False]):
        creatureList.append(Creature(1,Genome(secrets.token_hex(68)),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1)))
    else:
        creatureList.append(Creature(0,random.choice(initialGenomes),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1),))
board = Board(creatureList,boardHeight=boardHeight,boardWidth=boardWidth)
board.removeCollisions()

def getLocations(board):
    preyX = []
    preyY = []
    predX = []
    predY = []
    grassX = []
    grassY = []
    grassColors = []
    for creature in board.creatures:
        if creature.type == 0:
            preyX.append(creature.xpos)
            preyY.append(creature.ypos)
        else:
            predX.append(creature.xpos)
            predY.append(creature.ypos)
    for i in range(boardWidth):
        for j in range(boardHeight):
            grassX.append(i)
            grassY.append(j)
            grassColors.append(board.grassDistribution[j][i])

    return([preyX,preyY,grassX,grassY,grassColors,predX,predY])

timeX = []
popPreyY = []
popPredY = []
avgFullnessY = []
avgHealthY = []

fig, ax00 = plt.subplots()

def animate(i):
    board.updateBoard()
    locations = getLocations(board)
    x = locations[0]
    y = locations[1]
    grassX = locations[2]
    grassY = locations[3]
    grassColors = locations[4]
    predX = locations[5]
    predY = locations[6]
    ax00.clear()
    ax00.scatter(grassX,grassY,c=grassColors,cmap = 'Greens',marker='s',s=9)
    ax00.scatter(x,y,c='brown',s=9)
    ax00.scatter(predX,predY,c='red',s=9,marker='x')
    ax00.set_title('Day '+str(board.time)+", Season "+str(board.season))
    if board.time % 10 == 0:
        sampleCreature = random.choice(board.creatures)
        print("Sample Genome (Type %1d): "%sampleCreature.type+sampleCreature.Genome.code)


    #ax01.clear()
    timeX.append(board.time)
    
    avgFullnessY.append(np.mean([len(creature.Genome.code) for creature in board.creatures]))
    avgHealthY.append(np.mean([creature.litterSize for creature in board.creatures]))
    
    numPrey = 0
    numPred = 0
    for creature in board.creatures:
        if creature.type == 0:
            numPrey += 1
        else:
            numPred += 1
    popPreyY.append(numPrey)
    popPredY.append(numPred)

    #ax01.plot(timeX,popPreyY)
    #ax01.plot(timeX,popPredY)
    """ if len(timeX)<50:
        ax01.plot(timeX,popPreyY)
        ax01.plot(timeX,popPredY)
        
        
        ax10.clear()
        ax10.plot(timeX,avgFullnessY)
        

        ax11.clear()
        ax11.plot(timeX,avgHealthY)
        
    else:
        ax01.plot(timeX,popPreyY)
        ax01.plot(timeX,popPredY)
        
        
        ax10.clear()
        ax10.plot(timeX[-50:],avgFullnessY[-50:])
        

        ax11.clear()
        ax11.plot(timeX[-50:],avgHealthY[-50:]) """
    #ax01.set_title('Population over Time')
    """ ax10.set_title('Genome Size over Time')
    ax11.set_title('Litter Size over Time') """

   

ani = FuncAnimation(plt.gcf(), animate, interval=1)



plt.tight_layout()
plt.show()