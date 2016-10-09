import networkx as nx
import random
import pickle
import matplotlib.pyplot as plt

graph = nx.connected_caveman_graph(5,4)
mapping = dict((x,x+1) for x in graph.nodes())
graph = nx.relabel_nodes(graph, mapping)

V_P = graph.nodes()
V_L = [1, 6, 10, 14, 18]
E_P = graph.edges()
Budget=8
print V_P
print ""
print V_L
print ""
print E_P

node_colors = list()
for node in graph.nodes():
	if node in V_L:
		node_colors.append('g')
	else:
		node_colors.append('w')

C_P = 2
for (u,v) in graph.edges():
	graph.add_edge(u, v, weight=C_P)

nx.draw_networkx(graph, width=4, font_size=10, node_color=node_colors, node_size=500)
plt.show()

myDictionary = dict()
myDictionary['B'] = Budget
myDictionary['C_P'] = C_P
myDictionary['E_P'] = E_P
myDictionary['V_L'] = V_L
myDictionary['V_P'] = V_P

pickle.dump(myDictionary, open("../test_results/caveman/cavemanGraph1.p", "wb"))
