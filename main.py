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
initialGenomes.append(Genome("0d5bb261e978a32ddd208a97414afe81acdfcff9ea35a47ee5cdd71ae61a2c14edc3cc9415876fb162fb16b9451f776ade5d545feb03a765c071e5c5f567aab8e72bd77cb604101e9270245"))
initialGenomes.append(Genome("0de9e562c4240b26a4a74d4531deddf20156c8f9e1fd778bdb2f1fa6d8d5119e7c51d91f24f70b3110fa4815a4a5d5dc81361d42780ca643862f20387f0af234e590c8ed8e1e52ab9c"))
initialGenomes.append(Genome("29ced47663363a8e5262153f3535c25a0f60ef74496e168e18e1e7584b4c6e42bc3ed6d0b02ee8d00313e2791b6e5ff0366777b1c1db52a54ecf02ed477d1f270bf5991bf60af"))
initialGenomes.append(Genome("0faba9201c0963b4fcce5e81dfc69efa7b71827ad49cd659b00fb6dd5e557015fdf516f64981e3ca4f20f6118e8a79694bf375d5f8c63f0e021b71d58f80221fb7ad9e8c272a50165b827a9"))
initialGenomes.append(Genome("07fde580cd2862b4d494ca80fc8e5cd5b7c30af1ea47d20539d73699f656e46820d1ff871d43d1ca4f34761999a059c8a0b5d673e0802118503c83b0974ede74cd803defc3fa6686c75a501"))
initialGenomes.append(Genome("c43f38a3226b0cb2cd8922e3fa987c45f43ce98a9ed7603cb5cd97959ecc532f4c1d8df1dd2b929f1fef6bc854e70c5881d204fe783d2c4a223e36518bdb0b8a2f7798a53c79e"))
initialGenomes.append(Genome("1fffc520e46963a4d19086025f60e3cf114f0ad9e0b9760d99d2c9fe4bc5157c31d0fc871dc1a9c66f24f639218c7979e214fe75dc473f0c1219cd83d7c7aef1ed242ca283fef4165b3af1c7d6ae"))
initialGenomes.append(Genome("03de0e4524637964686b1f14e758fec5e977429eacc90104d7179faeae194f3edd59dbad62deefb22cece61848664ac772ffadbf7857dec40e1938b2f69edee229339fdabea937e39e6a8dd"))

creatureList = []
for i in range(100):
    #creatureList.append(Creature(0,Genome(secrets.token_hex(random.randint(18,58))),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1),))
    #creatureList.append(Creature(0,Genome("7fec28040b24107708310c007b623ab36562bc895bf006d6238a3ba743930768ea77c624fae4a4eafa42b7167b1867e0d2bcdad7f5eabdcd8ba4e6a009ba83cba8382a83"),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1),))
    creatureList.append(Creature(0,random.choice(initialGenomes),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1)))
    
    #if random.choice([True,False,False,False]):
    #    creatureList.append(Creature(1,Genome(secrets.token_hex(68)),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1)))
    #else:
    #    creatureList.append(Creature(0,random.choice(initialGenomes),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1),))
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
avgAgeY = []

fig, ([ax00,ax01],[ax10,ax11]) = plt.subplots(2,2)

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


    ax01.clear()
    timeX.append(board.time)
    
    avgFullnessY.append(np.mean([len(creature.Genome.code) for creature in board.creatures]))
    avgAgeY.append(np.mean([creature.age for creature in board.creatures]))
    
    numPrey = 0
    numPred = 0
    for creature in board.creatures:
        if creature.type == 0:
            numPrey += 1
        else:
            numPred += 1
    popPreyY.append(numPrey)
    popPredY.append(numPred)

    
    if len(timeX)<50:
        ax01.plot(timeX,popPreyY)
        ax01.plot(timeX,popPredY)
        
        
        ax10.clear()
        ax10.plot(timeX,avgFullnessY)
        

        ax11.clear()
        ax11.plot(timeX,avgAgeY)
        
    else:
        ax01.plot(timeX,popPreyY)
        ax01.plot(timeX,popPredY)
        
        
        ax10.clear()
        ax10.plot(timeX[-50:],avgFullnessY[-50:])
        

        ax11.clear()
        ax11.plot(timeX[-50:],avgAgeY[-50:])
    ax01.set_title('Population over Time')
    ax10.set_title('Genome Size over Time')
    ax11.set_title('Age over Time')

   

ani = FuncAnimation(plt.gcf(), animate, interval=1)



plt.tight_layout()
plt.show()