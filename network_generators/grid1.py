import networkx as nx
import random
import pickle
import matplotlib.pyplot as plt

N = 7

gridGraph = nx.grid_2d_graph(N,N)
newLabels = dict( ((i, j), i * N + j + 1) for i, j in gridGraph.nodes() )
gridGraph = nx.relabel_nodes(gridGraph,newLabels,copy=False)

V_P = gridGraph.nodes()
V_L = [3, 8, 14, 18, 29, 33, 44, 49]
E_P = gridGraph.edges()
Budget=24

node_colors = list()
for node in gridGraph.nodes():
	if node in V_L:
		node_colors.append('g')
	else:
		node_colors.append('w')

C_P = 2
for (u,v) in gridGraph.edges():
	gridGraph.add_edge(u, v, weight=C_P)

pos=dict()
currentNode = 1
x = y = 0
while x < N:
	while y < N:
		pos[currentNode] = (x,y)
		currentNode += 1
		y += 1
	y = 0
	x += 1

nx.draw_networkx(gridGraph, pos=pos, width=4, font_size=10, node_color=node_colors, node_size=500)
edge_labels = nx.get_edge_attributes(gridGraph,'weight')
nx.draw_networkx_edge_labels(gridGraph,pos=pos,edge_labels=edge_labels, font_size=10)
plt.show()

myDictionary = dict()
myDictionary['B'] = Budget
myDictionary['C_P'] = C_P
myDictionary['E_P'] = E_P
myDictionary['V_L'] = V_L
myDictionary['V_P'] = V_P

pickle.dump(myDictionary, open("../test_results/grid/grid1.p", "wb"))
