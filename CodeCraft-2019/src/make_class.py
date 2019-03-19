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
road = input_txt("../1-map-training-2/road.txt").reshape(-1, 7)
car = input_txt("../1-map-training-2/car.txt").reshape(-1, 5)
cross = input_txt("../1-map-training-2/cross.txt").reshape(-1, 5)

#计算每个起点中车的数量
to = []
for i in cross:
    count = 0
    for j in car:
        if j[2] == i[0]:
            count = count+1
    to.append(count)

n = 1
nodelm = []
for i in range(64):
    nodelm.append(n)
    n = n+1

G.add_nodes_from(nodelm, bipartite=0, _type='emp')

for i in road:
    if i[6] == 1:
        G.add_edge(i[4], i[5])
        G.add_edge(i[5], i[4])
    else:
        G.add_edge(i[4], i[5])

labels = dict((n, "(" + n + "," + d['_type'] + ")") for n, d in G.nodes(data=True))

# for i in road:
#     print(to[i[4]-1], to[i[5]-1])

# for i in road:
#     if i[6] == 1:
#         G.add_edge(to[i[4]-1], to[i[5]-1])
#         G.add_edge(to[i[5]-1], to[i[4]-1])
#     else:
#         G.add_edge(to[i[4]-1], to[i[5]-1])
#
# print(G.nodes())
# nx.draw_spectral(G, with_labels=True, node_color='y')
# plt.show()

plt.figure()
edges = G.edges()
nx.draw_networkx(G, edges=edges, labels=labels)
plt.show()






