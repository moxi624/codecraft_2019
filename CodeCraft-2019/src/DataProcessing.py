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
def map(number, matrix0, matrix1, matrix2):
    for i in range(number):
        for j in range(number):
            Dijkstra(number, matrix0, i + 1, j + 1, shortest_distance)  # 普通权重
            Dijkstra(number, matrix1, i + 1, j + 1, high_speed)  # 速度快
            Dijkstra(number, matrix2, i + 1, j + 1, slow_speed)  # 速度慢


map(cross_number, cross_adjacency_matrix, cross_adjacency_high_speed, cross_adjacency_slow_speed)
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

# 定义所有车辆终点数组
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

# 定义所有车辆起点数组
carStartPoint = []
for i in range(car_number):
    # 定义标志位，判断是否包含该元素
    tag = 0
    for j in range(len(carStartPoint)):
        if car[i][1] == carStartPoint[j]:
            tag = 1
            break
    if tag == 0:
        carStartPoint.append(car[i][1])

# 对终点数组进行排序
# carEndPoint = sorted(carEndPoint)

# 定义Map，存储相同终点的车辆， key：起点   value：该终点的所有车辆
endPointMap = {}
for i in range(len(carEndPoint)):
    tempCarInfoArray = []
    for j in range(car_number):
        if carEndPoint[i] == car[j][2]:
            tempCarInfoArray.append(car[j])
    endPointMap.setdefault(carEndPoint[i], tempCarInfoArray)

# 定义Map，存储相同终点的车辆， key：起点   value：该终点的所有车辆
startPointMap = {};
for i in range(len(carStartPoint)):
    tempCarInfoArray = []
    for j in range(car_number):
        if carStartPoint[i] == car[j][2]:
            tempCarInfoArray.append(car[j])
        startPointMap.setdefault(carStartPoint[i], tempCarInfoArray)

# 定义系统调度时间
totalTIme = 550

# 定义每个时间片调度时间
# step = int(totalTIme / endPointMap.keys().__len__())

planTime = 0
startMaxPlanTime = 0

# 已经出发的车辆
haveStartCar = []

# 获得每个分类的车辆出发时间片
for key, values in endPointMap.items():

    # 把该分类下的车取出来，和以该Key作为起点的车，取出来，合并成一个新的数组
    startPointCarList = startPointMap.get(key)
    mergeCarList = values + startPointCarList

    # 将要出发的车辆列表
    willStartCar = []

    # 判断该分类区间的车，是否有已经出发的车辆
    for item in mergeCarList:
        isStart = 0
        for startClassItem in haveStartCar:
            if item[0] == startClassItem:
                isStart = 1
                break
        if isStart == 0:
            willStartCar.append(item)

    # 将马上要出发的车，存入发车列表
    for car in willStartCar:
        haveStartCar.append(car[0])


    # 时间片大小进一步划分（根据驶入当前终点的车辆数，动态改变 ）  （总分片/ 总车辆 ）* 当前点车辆
    step = int((totalTIme / car_number) * len(values))
    # 太小的时间片，给一个默认值
    if step < 5:
        step = 5
    # 太大的时间片，是否也设置一个最大值呢？

    # 第一次读取最大的出发时间
    if startMaxPlanTime == 0:
        for item in willStartCar:
            if item[4] > startMaxPlanTime:
                startMaxPlanTime = item[4]
        planTime = startMaxPlanTime
    else:
        planTime += step
    print(planTime)
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
    for item in willStartCar:
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
