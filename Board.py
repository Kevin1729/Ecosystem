import numpy as np
import random
from Creature import Creature
from Genome import Genome
class Board:
    def __init__(self,creatureList,boardHeight=100,boardWidth=100):
        self.time = 0
        self.boardHeight = boardHeight
        self.boardWidth = boardWidth
        self.grassDistribution = 2*np.ones((self.boardHeight,self.boardWidth))
        self.creatures = creatureList

        
        self.creaturesDistribution = []
        for i in range(self.boardHeight):
            self.creaturesDistribution.append([])
        for sublst in self.creaturesDistribution:
            for j in range(self.boardWidth):
                sublst.append([])
        for creature in self.creatures:
            #to get creature at (x,y): creaturesDistribution[y][x][0]
            self.creaturesDistribution[creature.ypos][creature.xpos].append(creature)
            print("Added a creature at (" + str(creature.xpos)+","+str(creature.ypos)+")")

        self.season = 0 #0 = Spring, 1 = Summer, 2 = Autumn, 3 = Winter
    
    def removeCollisions(self):
        for i in range(self.boardHeight):
            for j in range(self.boardWidth):
                location = self.creaturesDistribution[i][j]
                while len(location) > 1:
                    replacee = random.choice(location)
                    location.remove(replacee)
                    #search for empty location with spiral:
                    spiralXStep = 1
                    spiralYStep = 1
                    spiralDirection = 1
                    foundLocation = False
                    while True:
                        #print("Searching for location!")
                        for xStep in range(spiralXStep):
                            replacee.xpos += spiralDirection
                            if replacee.xpos < 0 or replacee.xpos >= self.boardWidth or replacee.ypos < 0 or replacee.ypos >= self.boardWidth:
                                #print("Out of bounds!")
                                break
                            if len(self.creaturesDistribution[replacee.ypos][replacee.xpos])==0:
                                foundLocation = True
                                self.creaturesDistribution[replacee.ypos][replacee.xpos].append(replacee)
                                break
                        if foundLocation:
                            #print("Stopping search!")
                            break
                            

                        for yStep in range(spiralYStep):
                            replacee.ypos += spiralDirection
                            if replacee.xpos < 0 or replacee.xpos >= self.boardWidth or replacee.ypos < 0 or replacee.ypos >= self.boardWidth:                                
                                #print("Out of bounds!")
                                break
                            if len(self.creaturesDistribution[replacee.ypos][replacee.xpos])==0:
                                foundLocation = True
                                self.creaturesDistribution[replacee.ypos][replacee.xpos].append(replacee)
                                break
                        if foundLocation:
                            #print("Stopping search!")
                            break

                        spiralYStep += 1
                        spiralXStep += 1
                        spiralDirection *= -1
    def printCreatureMap(self):
        lst = []
        for i in range(self.boardHeight):
            lst.append([])


        for sublst in lst: 
            for j in range(self.boardWidth):
                sublst.append(0)   
        
        for i in range(self.boardHeight):
            for j in range(self.boardWidth):
                location = self.creaturesDistribution[i][j]
                if len(location)!=0:
                    lst[i][j]=len(location)
                
        for row in lst:
            print(row)
    def updateBoard(self):
        #Things to update, in order: 
        
        #Creature act
        #Remove dead
        #update creature distribution
        #Remove collisions
        #Time ++
        #Season ++
        #Grow Food 
        creatureNum = 1
        for creature in self.creatures:
            #sensory inputs:
            #relative xpos
            #relative ypos
            #relative age
            #relative health
            #relative fullness
            #relative energy
            #gestation stage
            #closest grass x
            #closest grass y
            #season
            #bias (always 1)
            #random (rng -1 to 1)
            #vision
            
            sensoryInput = []
            sensoryInput.append(creature.xpos/self.boardWidth)
            sensoryInput.append(creature.ypos/self.boardHeight)
            sensoryInput.append(creature.relativeAge)
            sensoryInput.append(creature.health/creature.healthCap)
            sensoryInput.append(creature.fullness/creature.fullnessCap)
            sensoryInput.append(creature.energy/creature.energyCap)
            sensoryInput.append(creature.gestationStage/creature.gestationPeriod)
            sensoryInput.append(random.uniform(-1,1))
            sensoryInput.append(random.uniform(-1,1))
            sensoryInput.append(self.season/4)
            sensoryInput.append(1)
            sensoryInput.append(random.uniform(-1,1))
            foundFood = False
            if creature.type != 0:
                nearestPrey = creature.getNearestCreature(self,searchType = 0)
                if nearestPrey != 0:
                    sensoryInput[7] = nearestPrey.xpos
                    sensoryInput[8] = nearestPrey.ypos
                foundFood = True
            for ring in range(creature.vision):

                x = creature.xpos + ring+1
                y = creature.ypos + 0
                
                for i in range(4*(ring+1)):
                    if x < 0 or y < 0 or x >= self.boardWidth or y >= self.boardHeight:
                        #print("Out of bounds!")
                        sensoryInput.append(0)
                    else:
                        if not foundFood:
                            if creature.type == 0:
                                if self.grassDistribution[y][x]!=0:
                                    sensoryInput[7] = x/creature.vision
                                    sensoryInput[8] = y/creature.vision
                                    foundFood = True
                            
                        
                        location = self.creaturesDistribution[y][x]
                        if len(location)==0:
                            sensoryInput.append(0)
                        else:
                            if location[0].type == creature.type:
                                sensoryInput.append(Genome.geneticSimilarity(creature.Genome,location[0].Genome))
                            else:
                                sensoryInput.append(-1)
                    if i < ring+1:
                        x -= 1
                        y += 1
                    elif i < (ring+1)*2:
                        x -= 1
                        y -= 1
                    elif i < (ring+1)*3:
                        x += 1
                        y -= 1
                    else:
                        x += 1
                        y += 1
            


            numpyArr = np.reshape(np.array(sensoryInput),(1,len(sensoryInput)))
            #print("---Creature "+str(creatureNum)+"---")
            creature.act(numpyArr,self)  
            
            creatureNum += 1


        #removing dead:
        for i in range(len(self.creatures)-1,-1,-1):
            if self.creatures[i].health <= 0 or self.creatures[i].age > 1.5*self.creatures[i].maxAge:
                self.creatures.pop(i)
        self.creaturesDistribution = []
        for i in range(self.boardHeight):
            self.creaturesDistribution.append([])
        for sublst in self.creaturesDistribution:
            for j in range(self.boardWidth):
                sublst.append([])
        for creature in self.creatures:
            #to get creature at (x,y): creaturesDistribution[y][x][0]
            self.creaturesDistribution[creature.ypos][creature.xpos].append(creature)
        self.removeCollisions()
        self.time += 1
        #self.season = (self.time // 20)%4
        grassGrowthProb = 0
        if self.season == 0:
            grassGrowthProb = 1/60
        elif self.season == 1:
            grassGrowthProb = 1/40
        elif self.season == 2:
            grassGrowthProb = 1/80
        elif self.season == 3:
            grassGrowthProb = 1/120
        grassGrowth = np.random.binomial(1, grassGrowthProb, size = (self.boardHeight,self.boardWidth))
        self.grassDistribution = np.minimum(np.add(self.grassDistribution,grassGrowth),3)
        #print(self.grassDistribution)