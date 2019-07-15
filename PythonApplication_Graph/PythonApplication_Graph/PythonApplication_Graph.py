#%matplotlib inline
import networkx as nx
import matplotlib.pyplot as plt
G=nx.Graph()
vlist = [1,2,3,4]
elist = [(1,2), (1,3), (2,3),(2,4),(3,4)]
G.add_nodes_from(vlist)
G.add_edges_from(elist)
nx.draw_networkx(G, node_color='lightgray', node_size=800)
plt.axis('off')
#plt.savefig('../fig/graph1.eps')
plt.show()
