from Genome import Genome
from Brain import Brain

class Creature:
    def __init__(self,type,Genome,xpos,ypos,age = 1):
        #11 attributes: Max Speed, Max Health, Max Fullness, Max Energy, Max Defense, Max Attack, Growth Rate, Gestation Period, Vision, Brain Speed, Litter Size

        self.type = type #0 = prey, 1 = predator
        self.Genome = Genome
        self.Brain = Brain(self.Genome)
        self.xpos = xpos
        self.ypos = ypos
        self.age = age
        

        #11 attributes: Max Speed, Max Health, Max Fullness, Max Energy, Max Defense, Max Attack, Max Age, Gestation Period, Vision, Brain Speed, Litter Size
        attributeCode = self.Genome.attributeCode
        self.maxSpeed = 1 + int(attributeCode[0],16)
        self.maxHealth = 10+10*int(attributeCode[1],16)
        self.maxFullness = 10+10*int(attributeCode[2],16)
        self.maxEnergy = 10+10*int(attributeCode[3],16)
        self.maxDefense = int(attributeCode[4],16)
        self.maxAttack = int(attributeCode[5],16)
        self.maxAge = 5 + 5*int(attributeCode[6],16)
        self.gestationPeriod = 5 + int(attributeCode[7],16)
        self.vision = 1 + int(self.Genome.attributeCode[8],16)//4
        self.brainSpeed = 1 + int(attributeCode[9],16)
        self.litterSize = 1 + int(attributeCode[10],16)//2

        self.relativeAge = min(1,self.age/self.maxAge)
        
        self.healthCap = max(10,self.relativeAge * self.maxHealth)
        self.health = self.healthCap

        
        self.fullnessCap = max(10,self.relativeAge * self.maxFullness)
        self.fullness = 10

        
        self.energyCap = self.maxEnergy
        self.energy = self.energyCap

        self.attack = self.relativeAge * self.maxAttack
        self.defense = self.relativeAge * self.maxDefense
        self.isPregnant = False
        self.currentMateGenome = 0
        self.gestationStage = 0
    
    def updateAge(self):
        self.age += 1
        self.relativeAge = min(1,self.age/self.maxAge)
        
        self.healthCap = max(10,self.relativeAge * self.maxHealth)
        
        self.fullnessCap = max(10,self.relativeAge * self.maxFullness)
        self.energyCap = self.maxEnergy

        self.attack = self.relativeAge * self.maxAttack
        self.defense = self.relativeAge * self.maxDefense
    def updateEFH(self):
        #EFH = Energy Fullness Health
        #self.fullness -= round(5*self.relativeAge)
        self.fullness -= 2
        if self.energy <= 0:
            self.fullness -=5
            self.energy = self.energyCap
        if self.isPregnant:
            self.fullness -= self.litterSize
        
        if self.fullness < 0:
            self.health = 0 #fuckem that's why
            #self.fullness = self.fullnessCap
            #self.energy = self.energyCap/2
        else:
            self.health = min(self.health+5,self.healthCap)
            #self.energy = self.energyCap
        #print("Energy:"+str(self.energy))
        #print("Fullness:" + str(self.fullness))
        #print("Health:"+ str(self.health))
        
    def getNearestCreature(self, board, searchType = -1):
        visionRadius = 1
        foundCreature = False
        retCreature = 0
        if searchType != 0 and searchType != 1:
            searchType = self.type
        for sightRing in range(self.vision):
            x = self.xpos+visionRadius
            y = self.ypos+0
            for i in range(4*visionRadius):
                #print("Searching (%1d,%1d)" % (x,y))
                
                if x < 0 or y < 0 or x >= board.boardWidth or y >= board.boardHeight:
                    #print("Out of bounds!")
                    pass
                else:
                    if len(board.creaturesDistribution[y][x]) != 0 and not foundCreature and board.creaturesDistribution[y][x][0].type == searchType:
                        #print("Found creature!")
                        retCreature = board.creaturesDistribution[y][x][0]
                        foundCreature = True
                    
                #print("(%1d,%1d)" % (x,y))
                if i < visionRadius:
                    x -= 1
                    y += 1
                elif i < visionRadius*2:
                    x -= 1
                    y -= 1
                elif i < visionRadius*3:
                    x += 1
                    y -= 1
                else:
                    x += 1
                    y += 1
                if foundCreature:
                    break
            if foundCreature:
                break
            visionRadius += 1
        return retCreature
    
    def act(self,sensoryInput, board):
        #print("Age: "+str(self.age)+"/"+str(self.maxAge))
        #print("Current Energy:" + str(self.energy))
        upkeep = 0
        for cost in self.Genome.attributeCode:
            upkeep += int(cost,16)/5
        upkeep *= self.relativeAge
        upkeep += len(self.Genome.code)//10
        upkeep = round(upkeep)
        self.energy = max(0,self.energy-upkeep)
        #print("Upkeep:" + str(upkeep))
        #print("Energy after Upkeep:" + str(self.energy))

        
        actionVector = self.Brain.think(sensoryInput)[0]
        #action encoding:
        #actionVector[0] -> xMovement
        #actionVector[1] -> yMovement
        #actionVector[2] -> Eat (if prey, always 1; if predator, attack nearest Creature of type prey)
        #actionVector[3] -> Mate w/ nearest Creature of same type
        if self.health > 0:
            if actionVector[2] > 0 or self.type == 0:
                self.eat(board)
                #print("Attempting Eating!")
        
            if actionVector[3] > 0:
                self.mate(board)
                #print("Attempting Mating!")
            
            diffX = actionVector[0]*self.maxSpeed
            
            diffY = actionVector[1]*self.maxSpeed

            #print("Hoping to move by ("+str(diffX)+","+str(diffY)+")")
            if abs(diffX)+abs(diffY) == 0:
                energyFactor = 0
            else:
                energyFactor = min(1, self.energy/(abs(diffX)+abs(diffY)))
            #print(energyFactor)
            self.move(round(diffX*energyFactor),round(diffY*energyFactor),board)
            #print("Moving!")
        self.updateAge()
        self.updateEFH()
        self.checkBirth(board)
        
        
    
    def eat(self, board):
        if self.type == 0:
            if board.grassDistribution[self.ypos][self.xpos] != 0:
                board.grassDistribution[self.ypos][self.xpos] -= 1
                self.fullness = min(self.fullness+30, self.fullnessCap)
                #print("Ate grass!")
        if self.type == 1:
            prey = self.getNearestCreature(board, 0)
            if prey != 0:
                prey.health -= max(self.attack - prey.defense,0)
                self.energy -= 10
                if prey.health < 0:
                    self.fullness = min(self.fullness+30, self.fullnessCap)
                    print("Ate meat!")
    def mate(self, board):
        #creatures can only mate if they're not pregnant, and they have reached half of max age
        if self.isPregnant or self.relativeAge<0.5:
            return 0
        mate = self.getNearestCreature(board,)
        if mate != 0:
            self.isPregnant = True #pratham face
            self.currentMateGenome = mate.Genome
    def move(self, diffX, diffY,board):
        self.xpos += diffX
        self.ypos += diffY
        #print("Moving by ("+str(diffX)+","+str(diffY)+")")
        self.xpos = max(min(self.xpos,board.boardWidth-1),0)
        self.ypos = max(min(self.ypos,board.boardHeight-1),0)
        self.energy -= abs(diffX)+abs(diffY)
        
    def checkBirth(self, board):
        if self.isPregnant and self.fullness>2*self.litterSize:
            #if self.gestationStage >= self.gestationPeriod and len(board.creatures)<=0.1*board.boardHeight*board.boardWidth:
            if self.gestationStage >= self.gestationPeriod and len(board.creatures)<=0.75*board.boardHeight*board.boardWidth:
                for i in range(self.litterSize):
                    recombinedGenome = Genome.getRecombinedGenome(self.Genome,self.currentMateGenome)
                    board.creatures.append(Creature(self.type,recombinedGenome.getMutatedGenome(),self.xpos,self.ypos,age=self.gestationPeriod))
                self.gestationStage = 0
                self.isPregnant = False
                #print("Creature at (%1d,%1d) gave birth to a litter of %1d after %2d days!" % (self.xpos,self.ypos,self.litterSize,self.gestationPeriod))
            else:
                self.gestationStage += 1
                self.fullness -= self.litterSize
    def getBrainSize(self):
        return len(self.Genome.code)