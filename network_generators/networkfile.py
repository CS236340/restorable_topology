import networkx as nx
import pickle
import matplotlib.pyplot as plt

V_P = range(1,17)
V_L = [1, 5, 12, 15]
E_P = [(1,2),(1,3),(2,4),(3,4),(3,8),(4,9),(5,6),(5,8),(6,7),(7,8),(7,13),(9,10),(9,11),(10,12),(11,12),(11,13),(13,14),(13,15),(14,16),(15,16)]
C_P = dict()
for (u,v) in E_P:
    C_P[(u,v)] = 4
B=12

graph = nx.Graph()
graph.add_nodes_from(V_P)
graph.add_edges_from(E_P)

node_colors = list()
for node in graph.nodes():
	if node in V_L:
		node_colors.append('g')
	else:
		node_colors.append('w')

nx.draw_networkx(graph, width=4, font_size=10, node_color=node_colors, node_size=500)
plt.show()

myDictionary = dict()
myDictionary['B']=4
myDictionary['C_P']=C_P
myDictionary['E_P']=E_P
myDictionary['V_L']=V_L
myDictionary['V_P']=V_P

pickle.dump(myDictionary, open("save.p", "wb"))
