import random
class Genome:
    GENESIZE = 5
    NUMATTRIBUTES = 11

    def __init__(self,code):
        #11 attributes: Max Speed, Max Health, Max Fullness, Max Energy, Max Defense, Max Attack, Growth Rate, Gestation Period, Vision, Brain Speed, Litter Size
        
        self.code = code
        self.attributeCode = code[:Genome.NUMATTRIBUTES]
        self.behaviorCode = code[Genome.NUMATTRIBUTES:]
        self.behaviorGenes = []
        for i in range(0,len(self.behaviorCode),Genome.GENESIZE):
            currentGene = self.behaviorCode[i:i+Genome.GENESIZE]
            #self.behaviorGenes.append(str(bin(int(currentGene,16)))[2:])
            self.behaviorGenes.append(str(format(int(currentGene,16),"0"+str(Genome.GENESIZE*4)+"b")))
    
    def geneticSimilarity(genome1,genome2):
        #outputs the similarity between two genomes
        diffCount = 0
        for i in range(min([len(genome1.code),len(genome2.code)])):
            if genome1.code[i]!=genome2.code[i]:
                diffCount += 1
        diffCount += abs(len(genome1.code)-len(genome2.code))
        #print(diffCount)
        return 1 - diffCount/max([len(genome1.code),len(genome2.code)])

    
    def getMutatedGenome(self,substitutionRate = 0.05,duplicationRate = 0.01,deletionRate = 0.01):
        #outputs a mutated Genome
        #codeExpanded = list(str(bin(int(self.code,16)))[2:])
        
            
        #newCode = str(format(int("".join(codeExpanded),2),"0"+str(len(self.code))+"x"))
        newCode = self.code

        dupeCount = 0
        delCount = 0
        for i in range(Genome.NUMATTRIBUTES,len(self.code),Genome.GENESIZE):
            currentGene = self.code[i:i+Genome.GENESIZE]

            #duplication
            if random.choices([False,True],[1-duplicationRate,duplicationRate])[0]:
                newCode += currentGene
                dupeCount += 1
                #print("Duped gene: " + currentGene)
            #deletion
            if random.choices([False,True],[1-deletionRate,deletionRate])[0]:
                indexOfGene = newCode.find(currentGene)
                newCode = newCode[:indexOfGene]+newCode[indexOfGene+Genome.GENESIZE:]
                delCount += 1
                #print("Deleted gene: " + currentGene)

        codeExpanded = list(str(format(int(newCode,16),"0"+str(4*len(newCode))+"b")))
        count = 0
        for i in range(len(codeExpanded)):
            if random.choices([False,True],[1-substitutionRate,substitutionRate])[0]:
                if codeExpanded[i]=="1":
                    codeExpanded[i] = "0"
                else:
                    codeExpanded[i] = "1"
                count+=1
        
        newCode = str(format(int("".join(codeExpanded),2),"0"+str(len(newCode))+"x"))

        #print(str(count)+" substitutions, " + str(dupeCount)+" duplications, " + str(delCount)+" deletions.")
        return Genome(newCode)


    def getRecombinedGenome(genome1,genome2):
        recombinedGenome = ""
        genome1BehaviorLength = len(genome1.behaviorGenes)
        genome2BehaviorLength = len(genome2.behaviorGenes)
        for i in range(Genome.NUMATTRIBUTES):
            if random.choices([True,False])[0]:
                #print("Taking from parent 1")
                recombinedGenome += genome1.attributeCode[i]
            else:
                #print("Taking from parent 2")
                recombinedGenome += genome2.attributeCode[i]
        for i in range(max(genome1BehaviorLength,genome2BehaviorLength)):
            if random.choices([True,False])[0]:
                if i < genome1BehaviorLength:
                    #print("Taking from parent 1")
                    recombinedGenome += str(format(int(genome1.behaviorGenes[i],2),"0"+str(Genome.GENESIZE)+"x"))
            else:
                if i < genome2BehaviorLength:
                    #print("Taking from parent 2")
                    recombinedGenome += str(format(int(genome2.behaviorGenes[i],2),"0"+str(Genome.GENESIZE)+"x"))
        return Genome(recombinedGenome)

class AttribCode:
    MAX_SPEED        = 0
    MAX_HEALTH       = 1
    MAX_FULLNESS     = 2
    MAX_ENERGY       = 3
    MAX_DEFENSE      = 4
    MAX_ATTACK       = 5
    GROWTH_RATE      = 6
    GESTATION_PERIOD = 7
    VISION           = 8
    BRAIN_SPEED      = 9
    LITTER_SIZE      = 10
