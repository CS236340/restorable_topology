import networkx as nx
import random
import pickle
import matplotlib.pyplot as plt

N = 6

graph = nx.Graph()
V_P = range(1,36)
V_L = [1, 35]
E_P = [(1,2),(2,3),(3,4),(4,5),(6,7),(7,8),(8,9),(9,10),(10,11),(12,13),(13,14),(14,15),(15,16),(18,19),(19,20),(20,21),(21,22),(24,25),(25,26),(26,27),(27,28),(30,31),(31,32),(32,33),(33,34),(34,35),(1,6),(5,11),(10,16),(11,17),(12,18),(17,23),(22,28),(23,29),(24,30),(29,35)]
Budget=200

for node in V_P:
	graph.add_node(node)
graph.add_edges_from(E_P)

node_colors = list()
for node in graph.nodes():
	if node in V_L:
		node_colors.append('g')
	else:
		node_colors.append('w')

C_P = dict()
for (u,v) in graph.edges():
	edgeCapacity = random.choice(range(2,15,2))
	graph.add_edge(u, v, weight=edgeCapacity)
	C_P[(u,v)] = edgeCapacity

pos=dict()
currentNode = 1
x = y = 0
while x < N:
	while y < N:
		if currentNode == 5:
			y += 1
			pos[currentNode] = (x,y)
			currentNode += 1
			break
		pos[currentNode] = (x,y)
		currentNode += 1
		y += 1
	y = 0
	x += 1

nx.draw_networkx(graph, pos=pos, width=4, font_size=10, node_color=node_colors, node_size=500)
edge_labels = nx.get_edge_attributes(graph,'weight')
nx.draw_networkx_edge_labels(graph,pos=pos,edge_labels=edge_labels, font_size=10)
plt.show()

myDictionary = dict()
myDictionary['B'] = Budget
myDictionary['C_P'] = C_P
myDictionary['E_P'] = E_P
myDictionary['V_L'] = V_L
myDictionary['V_P'] = V_P

pickle.dump(myDictionary, open("graph1.p", "wb"))
