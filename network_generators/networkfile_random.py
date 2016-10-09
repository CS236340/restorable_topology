import networkx as nx
import random
import pickle

numberOfNodes = 50
numberOfRouters = 15
edgeProbability = 0.1
budget=32

connected = False
while (connected == False):
    randomGraph = nx.binomial_graph(numberOfNodes, edgeProbability)
    connected = nx.is_connected(randomGraph)

V_P = range(0, numberOfNodes)
V_L = random.sample(V_P, numberOfRouters)
E_P = randomGraph.edges()
C_P = dict()
for (u,v) in E_P:
    C_P[(u,v)] = 4

print E_P, "\n\n", V_P

myDictionary = dict()
myDictionary['B'] = budget
myDictionary['C_P'] = C_P
myDictionary['E_P'] = E_P
myDictionary['V_L'] = V_L
myDictionary['V_P'] = V_P

pickle.dump(myDictionary, open("save.p", "wb"))
