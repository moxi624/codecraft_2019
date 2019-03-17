import pandas as pd
import numpy as np
from numpy.random import rand

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


car = input_txt("../config/car.txt").reshape(-1,5)
road = input_txt("../config/road.txt").reshape(-1,7)
cross = input_txt("../config/cross.txt").reshape(-1,5)

# 总路口数
cross_number = len(cross)
# 道路数量
road_number = len(road)
# 车的数量
car_number = len(car)

cross_adjacency_matrix = np.ones((cross_number, cross_number))
cross_adjacency_matrix = float('inf')*cross_adjacency_matrix
# 构建路口的邻接矩阵(数值为距离，-1为不连通）
for i in range(cross_number):
    for j in range(1, 5):
        if cross[i][j] == -1:
            continue
        for x in range(cross_number):
            for y in range(1, 5):
                if cross[i][j] == cross[x][y]:   # 找出相邻路口
                    for r in range(road_number):
                        if road[r][0] == cross[i][j] and i != x:
                            cross_adjacency_matrix[i][x] = road[r][1]   # 获得路口之间距离


# print(cross_adjacency_matrix)
# cam = pd.DataFrame(cross_adjacency_matrix)
# cam.to_csv('cam.csv')

# 用Dijkstra's Algorithm算法，计算出最短路径
def Dijkstra(points, graph, start, end):
    pre = [0] * (points + 1)  # 记录前驱
    vis = [0] * (points + 1)  # 记录节点遍历状态
    dis = [float('inf') for i in range(points + 1)]  # 保存最短距离
    road = [0] * (points + 1)  # 保存最短路径
    roads = []
    map = graph

    for i in range(points + 1):  # 初始化起点到其他点的距离
        if i == start:
            dis[i] = 0
        else:
            dis[i] = map[start][i]
        if map[start][i] != float('inf'):
            pre[i] = start
        else:
            pre[i] = -1
    vis[start] = 1
    for i in range(points + 1):  # 每循环一次确定一条最短路
        min = float('inf')
        for j in range(points + 1):  # 寻找当前最短路
            if vis[j] == 0 and dis[j] < min:
                t = j
                min = dis[j]
        vis[t] = 1  # 找到最短的一条路径 ,标记
        for j in range(points + 1):
            if vis[j] == 0 and dis[j] > dis[t] + map[t][j]:
                dis[j] = dis[t] + map[t][j]
                pre[j] = t
    p = end
    len = 0
    while p >= 1 and len < points:
        road[len] = p
        p = pre[p]
        len += 1
    mark = 0
    len -= 1
    while len >= 0:
        roads.append(road[len]+1)
        len -= 1
    print(str(start+1)+" 到 "+str(end+1))
    print("最短距离：", dis[end],end=" ")
    print("最短路径：", roads)



# 固定map图
def map():
    map = cross_adjacency_matrix
    for i in range(cross_number):
        for j in range(i+1, cross_number):
            Dijkstra(cross_number-1, map, i, j)
map()
