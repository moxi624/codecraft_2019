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
#print(road)

for i in road:
    if i[6] == 1:
        G.add_edge(i[4], i[5])
        G.add_edge(i[5], i[4])
    else:
        G.add_edge(i[4], i[5])



nx.draw_spectral(G, with_labels=True,)
plt.show()






