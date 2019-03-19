# import networkx as nx
# from networkx.algorithms import bipartite
# import matplotlib.pyplot as plt
#
# BG = nx.Graph()
#
#
#
# employees = [str(i) for i in range(3)]
# movies = ["mA", "mB", "mC"]
#
# BG.add_nodes_from(employees, bipartite=0, _type='emp')
# BG.add_nodes_from(movies, bipartite=1, _type='mov')
#
# edges = [("0", "mA"), ("0", "mC"), ("1", "mA"),("1", "mB"), ("2", "mA")]
# BG.add_edges_from(edges)
# labels = dict((n, "(" + n + "," + d['_type'] + ")") for n, d in BG.nodes(data=True))
#
# # # Setting up pos for drawing bipartite graph. See the reference for more info
# # X, Y = bipartite.sets(BG)
# # pos = dict()
# # pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
# # pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
#
# # plt.figure()
# edges = BG.edges()
# nx.draw_networkx(BG, edges=edges, labels=labels)
# plt.show()


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
G = nx.MultiDiGraph()

def input_txt(file_address):
    with open(file_address, "r") as f:
        str = f.read()
        str = str.replace("(", "")
        str = str.replace(")", "")
        str = str.replace("\n", ",")
        str = str.lstrip('#qwertyuiopasdfghjklzxcvbnm,QWERTYUIOPASDFGHJKLZXCVBNM')

    arr = str.split(',')
    Arr = np.array(arr)
    Arr = Arr.astype(int)
    return Arr
road = input_txt("../1-map-training-1/road.txt").reshape(-1, 7)
car = input_txt("../1-map-training-1/car.txt").reshape(-1, 5)
cross = input_txt("../1-map-training-1/cross.txt").reshape(-1, 5)

#计算每个起点中车的数量
to = []
for i in cross:
    count = 0
    for j in car:
        if j[2] == i[0]:
            count = count+1
    to.append(count)

for i in road:
    if i[6] == 1:
        G.add_edge(to[i[4]-1], to[i[5]-1])
        G.add_edge(to[i[5]-1], to[i[4]-1])
    else:
        G.add_edge(to[i[4]-1], to[i[5]-1])

print(G.nodes())
nx.draw_networkx(G, with_labels=True, node_color='y')
plt.show()







