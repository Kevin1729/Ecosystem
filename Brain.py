from Genome import Genome, AttribCode
import numpy as np
import random
class Brain:
    def __init__(self, Genome):
        self.Genome = Genome
        self.interneuron_activations_1H = np.random.uniform(-1.0,1.0,(1,16))

        visionRadius = 1 + int(self.Genome.attributeCode[8],16)//4

        self.numInputNeurons = (2 * visionRadius ** 2 + 2 * visionRadius) + 12

        self.IHAdjacencyMatrix = np.zeros((self.numInputNeurons + 16,16)) #input to hidden layer adjacency matrix
        
        self.HOAdjacencyMatrix = np.zeros((self.numInputNeurons + 16,4)) #hidden to output layer adjacency matrix
        

        #genome encoding:
        #0th digit indicates source type: 0 = input, 1 = hidden
        #1st-6th digit indicates node ID: 0-63 in decimal
        #7th digit indicates sink type: 0 = output, 1 = hidden
        #8th-11th digit indicates node ID: 0-63 in decimal
        #12th-19th digit indicates weight: 0-255 in decimal
        for gene in self.Genome.behaviorGenes:
            weight = (int(gene[12:],2)-128)/32 #0 to 255 changed to around -4 to 4
            inputID = int(gene[1:7],2)
            outputID = int(gene[8:12],2)
            if int(gene[0])==0:
                if int(gene[7])==0:
                    self.HOAdjacencyMatrix[16+inputID%self.numInputNeurons][outputID%4] += weight
                elif int(gene[7])==1:
                    self.IHAdjacencyMatrix[16+inputID%self.numInputNeurons][outputID] += weight
            elif int(gene[0])==1:
                if int(gene[7])==0:
                    self.HOAdjacencyMatrix[inputID%16][outputID%4] += weight
                elif int(gene[7])==1:
                    self.IHAdjacencyMatrix[inputID%16][outputID] += weight

    def think(self, sensoryInput):
        if np.size(sensoryInput) != self.numInputNeurons:
            print( "Bruh bad sensory inputs")
            return 0
        H = len(self.interneuron_activations_1H[0])
        inputVector = np.zeros((1, len(self.interneuron_activations_1H[0]) + len(sensoryInput[0])))
        inputVector[:, H:] = sensoryInput
        inputVector[:, :H] = self.interneuron_activations_1H
        for i in range(int(self.Genome.attributeCode[AttribCode.BRAIN_SPEED], 16) + 1):
            inputVector[:, :H] = np.tanh(np.matmul(inputVector, self.IHAdjacencyMatrix)) #1x32 times 32x16 
            #print("Fed forward")
        hiddenVector = inputVector
        outputVector = np.tanh(np.matmul(hiddenVector, self.HOAdjacencyMatrix)) #1x32 times 32x16
        return outputVector


