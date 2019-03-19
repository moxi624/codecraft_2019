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


car = input_txt("../config/car.txt").reshape(-1, 5)
road = input_txt("../config/road.txt").reshape(-1, 7)
cross = input_txt("../config/cross.txt").reshape(-1, 5)

# 总路口数
cross_number = len(cross)
# 道路数量
road_number = len(road)
# 车的数量
car_number = len(car)

cross_adjacency_matrix = np.ones((cross_number + 1, cross_number + 1))
cross_adjacency_matrix = float('inf') * cross_adjacency_matrix
cross_adjacency_high_speed = np.ones((cross_number + 1, cross_number + 1))
cross_adjacency_high_speed = float('inf') * cross_adjacency_matrix
cross_adjacency_slow_speed = np.ones((cross_number + 1, cross_number + 1))
cross_adjacency_slow_speed = float('inf') * cross_adjacency_matrix

# 构建路口的邻接矩阵(数值为距离，-1为不连通）
for i in range(cross_number):
    for j in range(1, 5):
        if cross[i][j] == -1:
            continue
        for x in range(cross_number):
            for y in range(1, 5):
                if cross[i][j] == cross[x][y]:  # 找出相邻路口
                    for r in range(road_number):
                        if road[r][0] == cross[i][j] and i != x:
                            if road[r][6] == 0 and road[r][5] == cross[i][0]:
                                continue
                            else:
                                cross_adjacency_matrix[i + 1][x + 1] = (
                                            road[r][1] / ((0.95) * road[r][2] * (road[r][3])))  # 获得路口之间权重
                                cross_adjacency_high_speed[i + 1][x + 1] = (
                                            10 / ((1.5) * road[r][2] * (road[r][3])))  # 速度块
                                cross_adjacency_slow_speed[i + 1][x + 1] = (road[r][2] / (road[r][3]))  # 速度慢

# print(cross_adjacency_matrix)
# print(cross_adjacency_high_speed)
# print(cross_adjacency_slow_speed)
# cam = pd.DataFrame(cross_adjacency_matrix)
# cam.to_csv('cam.csv')

# 最短距离字典
shortest_distance = {}
# 速度最快字典
high_speed = {}
# 速度慢字典
slow_speed = {}


# 用Dijkstra's Algorithm算法，计算出最短路径
def Dijkstra(points, graph, start, end, dictionary):
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
        # 找到最短的一条路径 ,标记
        vis[t] = 1
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
        roads.append(road[len])
        len -= 1
    # print(str(start+1)+" 到 "+str(end+1))
    # print("最短距离：", dis[end],end=" ")
    # print("最短路径：", roads)

    dictionary[str(start) + '-' + str(end)] = roads


# 固定map图
def map():
    for i in range(cross_number):
        for j in range(cross_number):
            Dijkstra(cross_number, cross_adjacency_matrix, i + 1, j + 1, shortest_distance)  # 普通权重
            Dijkstra(cross_number, cross_adjacency_high_speed, i + 1, j + 1, high_speed)  # 速度快
            Dijkstra(cross_number, cross_adjacency_slow_speed, i + 1, j + 1, slow_speed)  # 速度慢


map()
# print(shortest_distance)
# print(high_speed)
# print((slow_speed))
# 路口->道路的字典
cross_road = {}
for i in range(road_number):
    if road[i][6] == 1:
        cross_road[str(road[i][4]) + '-' + str(road[i][5])] = road[i][0]
        cross_road[str(road[i][5]) + '-' + str(road[i][4])] = road[i][0]
    else:
        cross_road[str(road[i][4]) + '-' + str(road[i][5])] = road[i][0]
# print(cross_road)


# 生成每辆车路径
answer = []  # 普通路径
answer_high_speed = []  # 速度块的路径
answer_slow_speed = []  # 速度慢的路径


def generating_path(path,node):
    for i in range(car_number):
        every_answer = [car[i][0], car[i][4]]
        walk = node[str(car[i][1]) + '-' + str(car[i][2])]
        for j in range(len(walk) - 1):
            every_answer.append(cross_road[str(walk[j]) + '-' + str(walk[j + 1])])
        path.append(every_answer)

# 正常的
# generating_path(answer, shortest_distance)
#速度最快的
generating_path(answer_high_speed, high_speed)
#速度最慢的
generating_path(answer_slow_speed, slow_speed)

# print(answer)
# print(answer_high_speed)
# print(answer_slow_speed)

# 定义字典，用于存储每个车的正常行驶路径
answerMap = {}
# for item in answer:
#     answerMap.setdefault(item[0], item)

# 定义字典，用于存储每个车的高速行驶路径
answerHighMap = {}
for item in answer_high_speed:
    answerHighMap.setdefault(item[0], item)

# 定义字典，用于存储每个车的低速行驶路径
answerSlowMap = {}
for item in answer_slow_speed:
    answerSlowMap.setdefault(item[0], item)

# 定义所有车辆起点数组
carEndPoint = []
for i in range(car_number):
    # 定义标志位，判断是否包含该元素
    tag = 0
    for j in range(len(carEndPoint)):
        if car[i][2] == carEndPoint[j]:
            tag = 1
            break
    if tag == 0:
        carEndPoint.append(car[i][2])

# 对终点数组进行排序
carEndPoint = sorted(carEndPoint)

# 定义Map，存储相同终点的车辆， key：起点   value：该终点的所有车辆
endPointMap = {};
for i in range(len(carEndPoint)):
    tempCarInfoArray = []
    for j in range(car_number):
        if carEndPoint[i] == car[j][2]:
            tempCarInfoArray.append(car[j])
    endPointMap.setdefault(i, tempCarInfoArray)

# 定义系统调度时间
totalTIme = 500

# 定义每个时间片调度时间
step = int(totalTIme / endPointMap.keys().__len__())

planTime = 0
startMaxPlanTime = 0

# 获得每个分类的车辆出发时间片
for key, values in endPointMap.items():
    # 第一次读取最大的出发时间
    if startMaxPlanTime == 0:
        for item in values:
            if item[4] > startMaxPlanTime:
                startMaxPlanTime = item[4]
        planTime = startMaxPlanTime
    else:
        planTime += step

    # plan A 并发发车
    # for item in values:
    #     carId = item[0]
    #     car = answerMap.get(carId)
    #     car[1] = planTime
    #     answerMap.setdefault(carId, car)

    # planB 分片发车
    #  对每个时间片，在进行切割
    # itemPlanTime = int(step / len(values))
    # for item in values:
    #     # 得到车辆的ID
    #     carId = item[0]
    #     car = answerMap.get(carId)
    #     # 修改车辆的planTime
    #     car[1] = planTime + itemPlanTime
    #     answerMap.setdefault(carId, car)

    # planC 快车先行
    #     # 得到所有车的速度数组
    speedArray = []
    maxSpeed = 0
    for item in values:
        carSpeed = item[3]
        flag = 0
        for tempSpeed in speedArray:
            if tempSpeed == carSpeed:
                flag = 1
        if flag == 0:
            speedArray.append(carSpeed)

    for speed in speedArray:
        if speed > maxSpeed:
            maxSpeed = speed
    halfMaxSpeed = int(maxSpeed/2)
    for item in values:
        # 得到车辆的ID
        carId = item[0]
        carSpeed = item[3]

        # 对速度划分为两部分，低速车走低速车道，高速车走高速车道（这里低速和高速指的是权值）
        if halfMaxSpeed > carSpeed:
            # 走快速车道
            car = answerHighMap.get(carId)
        else:
            # 走低速车道
            car = answerSlowMap.get(carId)

        # 修改车辆的planTime   当前时间片 + 最高速度 - 车辆当前速度
        # 这样能够让速度快的车辆，优先先行，慢车就会排在快车的后面
        car[1] = planTime + maxSpeed - carSpeed
        answerMap.setdefault(carId, car)

result = []
for item in answerMap.values():
    result.append(item)


def output_txt(file_address, answer):
    with open(file_address, "w") as f:
        f.writelines("#(carId,StartTime,RoadId...)")
        f.writelines("\n")
        for j in answer:
            datastr = str(j)
            datastr = datastr.replace("[", "(")
            datastr = datastr.replace("]", ")")
            # print(datastr)
            f.writelines(datastr)
            f.writelines("\n")


output_txt("../config/answer.txt", result)
