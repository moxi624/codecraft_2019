import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
G = nx.MultiDiGraph()

#读取txt文件
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

#计算每个节点中车的数量
tolm = []
for i in cross:
    count = 0
    for j in car:
        if j[2] == i[0]:
            count = count+1
    tolm.append(str(count))
# print(tolm)
fromlm = []
for i in cross:
    count = 0
    for j in car:
        if j[1] == i[0]:
            count = count+1
    fromlm.append(str(count))
#print(fromlm)
# 设计节点编号
nodelm = []
m = 1
for i in range(64):
    nodelm.append(m)
    m = m+1

for i in range(64):
    G.add_node(nodelm[i], bipartite=0, _type=tolm[i])

#以添加边的形式画图
for i in road:
    if i[6] == 1:
        G.add_edge(i[4], i[5])
        G.add_edge(i[5], i[4])
    else:
        G.add_edge(i[4], i[5])

labels = dict((n, "(" + str(n) + "," + d['_type'] + ")") for n, d in G.nodes(data=True))

plt.figure()
edges = G.edges()
nx.draw_spectral(G, edges=edges, labels=labels, node_color='y')
plt.show()





