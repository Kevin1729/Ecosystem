from pyvis.network import Network
from Brain import Brain
from Genome import Genome
import numpy as np


genomeCode = "0fd63aa1d0b8b8cc9b2c6c073d1fbb7615e8e465b497fb1f9ffd88162f97f3194db64186cee3694ac55c6c8751fbcde4d0077d9bdc65c5263264c1eb87833455742737317d9a598f77"

brain = Brain(Genome(genomeCode))

net = Network(layout=True,height=1000,width=1000,)
net.toggle_drag_nodes(False)

nodes = []
nodeLevel = []
nodeLabels = ["xpos","ypos","rAge","rHealth","rFullness","rEnergy","gStage","grassX","grassY","season","bias","rng"]
for i in range(brain.numInputNeurons-12):
    nodeLabels.append("vis"+str(i))
for i in range(brain.numInputNeurons):
    nodes.append('I'+str(i))
    nodeLevel.append(1)
    net.add_node('I'+str(i),label=nodeLabels[i],level=1)

hiddenNeurons = []
hiddenLevel = []
for i in range(16):
    hiddenNeurons.append('H'+str(i))
    hiddenLevel.append(2)
    net.add_node('H'+str(i),level=2)

outputNeurons = []
outputLevel = []
outputLabels = ["moveX","moveY","Eat","Mate"]
for i in range(4):
    outputNeurons.append('O'+str(i))
    outputLevel.append(3)
    net.add_node('O'+str(i),label = outputLabels[i],level=3)


""" net.add_nodes(nodes,label = nodeLabels, level = nodeLevel,)
net.add_nodes(hiddenNeurons, level = hiddenLevel)
net.add_nodes(outputNeurons, level = outputLevel, label = outputLabels) """

#net.add_edge('I0','I0',width = 4,color = 'red')
(IHrows,IHcolumns) = np.shape(brain.IHAdjacencyMatrix)
print(str(IHrows)+","+str(IHcolumns))

for i in range(IHrows):
    for j in range(IHcolumns):
        weight = brain.IHAdjacencyMatrix[i][j]
        if weight != 0:
            if weight < 0:
                    color = 'red'
            else:
                color = 'blue'
            if i < 16:
                
                net.add_edge('H'+str(i),'H'+str(j),value = abs(brain.IHAdjacencyMatrix[i][j]),color = color)
                
            else:
                net.add_edge('I'+str(i-16), 'H' + str(j),value = abs(brain.IHAdjacencyMatrix[i][j]),color = color )
            print(weight)
(HOrows,HOcolumns) = np.shape(brain.HOAdjacencyMatrix)

for i in range(HOrows):
    for j in range(HOcolumns):
        weight = brain.HOAdjacencyMatrix[i][j]
        if weight != 0:
            if weight < 0:
                color = 'red'
            else:
                color = 'blue'
            if i < 16:
                net.add_edge('H'+str(i),'O'+str(j),value = abs(brain.HOAdjacencyMatrix[i][j]),color = color)
            else:
                net.add_edge('I'+str(i-16),'O'+str(j),value = abs(brain.HOAdjacencyMatrix[i][j]),color = color)
            print(weight)
net.show('mygraph.html')