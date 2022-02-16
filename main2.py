import numpy as np
from Creature import Creature
from Genome import Genome
from Board import Board
import secrets
import random

import time
start_time = time.time()
boardHeight = 100
boardWidth = 100
initialGenomes = []
initialGenomes.append(Genome("09dfb7788f504bb0a068cb59dbb222e684021f3ee88f74476ddf1028f2831186fce2897d0ebd8"))
initialGenomes.append(Genome("49fd3fe26c103e27628c60497b25889a1f561e838e65ef83e4b9aa85bafda93a93d1694799fbe"))
initialGenomes.append(Genome("a4d98ec24f60fea6d41ac9a37351272f169d2d327cc2afd33dda1a1beefa9217c0d0abdc"))
initialGenomes.append(Genome("68fd3fc07c9008d6555a3c6b59445bd26ae8f6038e8e167b7f96b4a803a1a91274feffca45bd3"))
initialGenomes.append(Genome("0cf676c03c006ea3116d00327920e77c5a066596b0c5c14766e55c03b23e42e4d60043ef0ab88c89ad"))

creatureList = []
for i in range(800):
    #creatureList.append(Creature(0,Genome(secrets.token_hex(38)),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1),))
    #creatureList.append(Creature(0,Genome("7fec28040b24107708310c007b623ab36562bc895bf006d6238a3ba743930768ea77c624fae4a4eafa42b7167b1867e0d2bcdad7f5eabdcd8ba4e6a009ba83cba8382a83"),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1),))
    #creatureList.append(Creature(random.choice([0,1]),random.choice(initialGenomes),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1)))
    
    if random.choice([False,False,False,False]):
        creatureList.append(Creature(1,Genome(secrets.token_hex(68)),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1)))
    else:
        creatureList.append(Creature(0,random.choice(initialGenomes),random.randint(0,boardWidth-1),random.randint(0,boardHeight-1),))
board = Board(creatureList,boardHeight=boardHeight,boardWidth=boardWidth)
board.removeCollisions()
for i in range(100):
    board.updateBoard()
    print(i)
print("--- %s seconds ---" % (time.time() - start_time))