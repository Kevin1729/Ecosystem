from pyvis.network import Network
from Brain import Brain
from Genome import Genome


genomeCode = "11fde1700521c32856d53dc24f4e8c722f9df4a58360cf9bfd512c357db73d4984589c1e0900"

brain = Brain(Genome(genomeCode))

net = Network()

nodes = []

for i in range(brain.numInputNeurons):
    nodes.append(i)

nodeLabels = ["xpos","ypos","rAge","rHealth","rFullness","rEnergy","gStage","grassX","grassY","season","bias","rng"]

for i in range(brain.numInputNeurons-12):
    nodeLabels.append("vis"+str(i))



net.add_nodes(nodes,label = nodeLabels)

net.add_edge(0,1,width = 4,color = 'red')

net.show('mygraph.html')