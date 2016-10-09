import matplotlib.pyplot as plt
import networkx as nx

def printGirdGraph(graph, N, V_L, edgeCapacity):
	graphCopy = graph.copy()
	nodes = graphCopy.nodes()
	edges = graphCopy.edges()

	node_colors = list()
	for node in nodes:
		if node in V_L:
			node_colors.append('g')
		else:
			node_colors.append('w')
	
	for (u,v) in edges:
		graphCopy.add_edge(u, v, weight=edgeCapacity)

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

	nx.draw_networkx(graphCopy, pos=pos, width=4, font_size=10, node_color=node_colors, node_size=500)
	edge_labels = nx.get_edge_attributes(graphCopy,'weight')
	nx.draw_networkx_edge_labels(graphCopy,pos=pos,edge_labels=edge_labels, font_size=10)
	plt.show()
