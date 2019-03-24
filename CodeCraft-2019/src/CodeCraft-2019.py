import logging
import sys
# to read input file
import pandas as pd
import numpy as np
from numpy.random import rand
import datetime
from multiprocessing import Manager
from multiprocessing import Process

import math

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


def output_txt(file_address, answer):
    with open(file_address, "w") as f:
        for j in answer:
            datastr = str(j)
            datastr = datastr.replace("[", "(")
            datastr = datastr.replace("]", ")")
            f.writelines(datastr)
            f.writelines("\n")




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
        roads.append(road[len])
        len -= 1
    # print(str(start+1)+" 到 "+str(end+1))
    # print("最短距离：", dis[end],end=" ")
    # print("最短路径：", roads)
    dictionary[str(start) + '-' + str(end)] = roads


# 固定map图
def map(cross_number, matrix, dictionary):
    for i in range(cross_number):
        for j in range(cross_number):
            Dijkstra(cross_number, matrix, i + 1, j + 1, dictionary)  # 普通权重


def cross_frequency(cross_number):
    # 记录节点使用的频率
    global count_cross_frequency
    count_cross_frequency = np.zeros(cross_number + 1)  # 以1作为起始位置
    return count_cross_frequency

#记录道路使用次数
def road_frequency(road_number):
    global count_road_frequency
    count_road_frequency = np.zeros(road_number)
    return count_road_frequency


def generating_path(car_number, path, node, cross_road, count_road_frequency,count_cross_frequency):  # node:生成车辆的节点路径
    for i in range(car_number):
        every_answer = [car[i][0], car[i][4]]
        walk = node[str(car[i][1]) + '-' + str(car[i][2])]
        for j in range(len(walk) - 1):
            count_cross_frequency[walk[j]] += 1
            count_road_frequency[(cross_road[str(walk[j]) + '-' + str(walk[j + 1])])-road[0][0]] += 1
            every_answer.append(cross_road[str(walk[j]) + '-' + str(walk[j + 1])])  # 将2节点通过字典转化为中间的道路ID
        path.append(every_answer)


logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

car = []
road = []
cross = []
answerPath = ""

# 将车辆分类成南北车辆  和 东西车辆
def direction(cross_number, car, answer):
    NorthAndSouthCarArray = []
    EastAndWestCarArray = []
    for i in range(len(car)):
        width=math.sqrt(cross_number)
        x = int(car[i][1])
        y = int(car[i][2])
        if x-int(x/width)*width == 0:
            x_du = x-int(x/width)*width + width
        else:
            x_du = x - int(x / width) * width
        if y-int(y/width)*width == 0:
            y_du = y-int(y/width)*width + width
        else:
            y_du = y - int(y / width) * width
        if x-(width*(5/8)*width) < y < x+(width*(5/8)**width):
            if x_du <= y_du:
                # 北
                NorthAndSouthCarArray.append(car[i])
            else:
                #南
                NorthAndSouthCarArray.append(car[i])
        else:
            if x <= y:
                #东
                EastAndWestCarArray.append(car[i])
            else:
                #西
                EastAndWestCarArray.append(car[i])
    directionMap = {}
    directionMap.setdefault("NorthAndSouth", NorthAndSouthCarArray)
    directionMap.setdefault("EastAndWest", EastAndWestCarArray)
    return directionMap


def main():
    start = datetime.datetime.now()
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    global car
    global road
    global cross
    global answerPath

    car = input_txt(car_path).reshape(-1, 5)
    road = input_txt(road_path).reshape(-1, 7)
    cross = input_txt(cross_path).reshape(-1, 5)
    answerPath = answer_path

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    # 总路口数
    cross_number = len(cross)
    # 道路数量
    road_number = len(road)
    # 车的数量
    car_number = len(car)

    cross_frequency(cross_number)#初始化count_cross_frequency
    road_frequency(road_number)#初始化count_cross_frequency

    cross_adjacency_matrix = np.ones((cross_number + 1, cross_number + 1))
    cross_adjacency_matrix = float('inf') * cross_adjacency_matrix
    cross_adjacency_high_speed = np.ones((cross_number + 1, cross_number + 1))
    cross_adjacency_high_speed = float('inf') * cross_adjacency_high_speed
    cross_adjacency_slow_speed = np.ones((cross_number + 1, cross_number + 1))
    cross_adjacency_slow_speed = float('inf') * cross_adjacency_slow_speed
    cross_adjacency_infrequent = np.ones((cross_number + 1, cross_number + 1))
    cross_adjacency_infrequent = float('inf') * cross_adjacency_infrequent
    cross_adjacency_wide_road = np.ones((cross_number + 1, cross_number + 1))
    cross_adjacency_wide_road = float('inf') * cross_adjacency_wide_road

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
                                            road[r][1] / (0.95 * road[r][2] * (road[r][3])))  # 获得路口之间距离
                                    cross_adjacency_high_speed[i + 1][x + 1] = (
                                            10 / (1.5 * road[r][2] * (road[r][3])))  # 速度块
                                    cross_adjacency_slow_speed[i + 1][x + 1] = (road[r][2] / (road[r][3]))  # 速度慢
                                    cross_adjacency_wide_road[i + 1][x + 1] = 10/road[r][3]
    # 重新评估权重2019-3-18
    # print(cross_adjacency_wide_road)
    # print(cross_adjacency_matrix)
    # print(cross_adjacency_infrequent)
    # cam = pd.DataFrame(cross_adjacency_matrix)
    # cam.to_csv('cam.csv')

    end1 = datetime.datetime.now()-start
    print(end1)#0.282849s

    # 生成经过cross的路线

    # 最短距离节点路径字典
    shortest_distance = Manager().dict()
    # 速度最快节点路径字典
    high_speed = Manager().dict()
    # 速度最慢节点路径字典
    slow_speed = Manager().dict()
    # 频率低节点路径字典
    low_frequency = Manager().dict()
    # 道路宽的路径字典
    wide_road = {}

    p1 = Process(target=map,args=(cross_number, cross_adjacency_matrix,shortest_distance))#普通路线
    p2 = Process(target=map,args=(cross_number, cross_adjacency_high_speed, high_speed))  # 速度最快路线
    p3 = Process(target=map,args=(cross_number, cross_adjacency_slow_speed, slow_speed))  # 速度最慢路线
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    # map(cross_number, cross_adjacency_wide_road, wide_road)  # 路最的宽路线
    # print(high_speed)
    end2 = datetime.datetime.now() - start
    print(end2)#1.59.01s

    # 路口->道路的字典
    cross_road = {}
    for i in range(road_number):
        if road[i][6] == 1:
            cross_road[str(road[i][4]) + '-' + str(road[i][5])] = road[i][0]
            cross_road[str(road[i][5]) + '-' + str(road[i][4])] = road[i][0]
        else:
            cross_road[str(road[i][4]) + '-' + str(road[i][5])] = road[i][0]

    answer = []  # 普通路径
    answer_high_speed = []  # 速度块的路径
    answer_slow_speed = []  # 速度慢的路径
    answer_low_frequency = []  # 频率低的路径
    answer_wide_road = [] # 道路宽的路径

    # 生成每辆车的road路径
    generating_path(car_number, answer, shortest_distance, cross_road,
                    count_road_frequency,count_cross_frequency)#普通路线
    generating_path(car_number, answer_high_speed, high_speed, cross_road,
                    count_road_frequency,count_cross_frequency)  # 速度最快路线
    generating_path(car_number, answer_slow_speed, slow_speed, cross_road,
                    count_road_frequency,count_cross_frequency)  # 速度最慢路线
    # generating_path(car_number, answer_wide_road, wide_road, cross_road,
    #                 count_road_frequency, count_cross_frequency)  # 道路宽路线

    end3 = datetime.datetime.now() - start
    print(end3)#2.03.45

    ###################################方向车辆################

    # key：东西，南北    value：东西南北车辆Array
    directionMap = direction(cross_number, car, answer)

    ###################################方向车辆################



    ################################频率最低路线生成###########################################
    for i in range(int(road_number / 3)):  # 设置：取消道路行驶权占总道路的比例
        max_frequency_road = 0
        index_frequency_road = 0
        for i in range(len(count_road_frequency)):
            if count_road_frequency[i] < float('inf'):
                if count_road_frequency[i] > max_frequency_road:
                    max_frequency_road = count_road_frequency[i]
                    index_frequency_road = i
        count_road_frequency[index_frequency_road] = 999999
    # print(count_road_frequency)

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
                                    cross_adjacency_infrequent[i + 1][x + 1] = count_road_frequency[r]/road[r][3] # 行驶次数最少的路

    # 低频路线，取消频率过高路线的行驶权
    # for item in cross_adjacency_infrequent
    #     if item >= cross_adjacency_infrequent.reshape(1,-1)

    map(cross_number, cross_adjacency_infrequent, low_frequency)  # 频率低的路线
    #print(count_cross_frequency)
    generating_path(car_number, answer_low_frequency, low_frequency, cross_road
                    , count_road_frequency, count_cross_frequency)  # 频率低的路线

    end4 = datetime.datetime.now() - start
    print(end4)
    #################################频率最低路线生成################################################

    # 定义答案Map
    answerMap = {}

    # 定义字典，用于存储每个车的行驶路径
    answerNormalMap = {}
    for item in answer:
        answerNormalMap.setdefault(item[0], item)

    # 定义字典，用于存储每个车的高速行驶路径
    answerHighMap = {}
    for item in answer_high_speed:
        answerHighMap.setdefault(item[0], item)

    # 定义字典，用于存储每个车的低速行驶路径
    answerSlowMap = {}
    for item in answer_slow_speed:
        answerSlowMap.setdefault(item[0], item)

    # 定义字典，用于存储每个车的低频率行驶路径
    answerLowFrequencyMap = {}
    for item in answer_low_frequency:
        answerLowFrequencyMap.setdefault(item[0], item)

    # 定义字典，用于存储每个车的道路最宽行驶路径
    answerWideRoadMap = {}
    for item in answer_wide_road:
        answerWideRoadMap.setdefault(item[0], item)

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

    # 定义所有车辆距离数组
    carDistancePoint = []
    for i in range(car_number):
        # 定义标志位，判断是否包含该元素
        tag = 0
        for j in range(len(carStartPoint)):
            if car[i][1] == carStartPoint[j]:
                tag = 1
                break
        if tag == 0:
            carStartPoint.append(car[i][1])


    # 定义所有车辆计划出发时间的数组集合
    # carPlanTimePoint = []
    # for i in range(car_number):
    #     # 定义标志位，判断是否包含该元素
    #     tag = 0
    #     for j in range(len(carPlanTimePoint)):
    #         if car[i][4] == carPlanTimePoint[j]:
    #             tag = 1
    #             break
    #     if tag == 0:
    #         carPlanTimePoint.append(car[i][4])



    # 定义Map，存储相同终点的车辆， key：终点   value：该终点的所有车辆
    endPointMap = {}
    for i in range(len(carEndPoint)):
        tempCarInfoArray = []
        for j in range(car_number):
            if carEndPoint[i] == car[j][2]:
                tempCarInfoArray.append(car[j])
        endPointMap.setdefault(i, tempCarInfoArray)

    # 定义Map，存储相同起点的车辆， key：起点   value：该起点的所有车辆
    startPointMap = {}
    for i in range(len(carStartPoint)):
        tempCarInfoArray = []
        for j in range(car_number):
            if carStartPoint[i] == car[j][2]:
                tempCarInfoArray.append(car[j])
        startPointMap.setdefault(carStartPoint[i], tempCarInfoArray)

    # 定义Map，存储相同计划出发时间的车辆， key：计划出发时间   value：该计划出发时间的所有车辆
    # planTimePointMap = {}
    # for i in range(len(carPlanTimePoint)):
    #     tempCarInfoArray = []
    #     for j in range(car_number):
    #         if carPlanTimePoint[i] == car[j][4]:
    #             tempCarInfoArray.append(car[j])
    #     planTimePointMap.setdefault(carPlanTimePoint[i], tempCarInfoArray)

    # 定义Map，存储车辆起始距离的车辆， key：距离范围   value：该距离范围内所有车辆
    distancePointMap = {}
    for i in range(len(carStartPoint)):
        tempCarInfoArray = []
        for j in range(car_number):
            if carStartPoint[i] == car[j][2]:
                tempCarInfoArray.append(car[j])
                distancePointMap.setdefault(carStartPoint[i], tempCarInfoArray)

    ####################################################以东西南北进行划分##############################################

    planTime = 0
    # 是否第一次发车
    firstStartCar = 0
    for key, values in directionMap.items():
        # 对所有南北  和 东西的车辆进行按速度分类

        # 得到所有车的速度数组
        speedArray = []
        maxSpeed = 0
        for item in values:
            carSpeed = item[3]
            flag = 0
            for tempSpeed in speedArray:
                if tempSpeed == carSpeed:
                    flag = 1
            if flag == 0:
                # 得到最高速度
                if carSpeed > maxSpeed:
                    maxSpeed = carSpeed
                speedArray.append(carSpeed)

        # 对距离进行划分

        halfMaxSpeed = int( maxSpeed/ 2)

        # 车辆发车计数器
        carStartCount = 0

        shardCount = 80
        #按照速度划分
        for item in values:

            if carStartCount >= shardCount:
                planTime += 4
                carStartCount = 0

            # 得到车辆的ID
            carId = item[0]
            carSpeed = item[3]

            # 按照速度划分
            if carSpeed < halfMaxSpeed:
                car = answerHighMap.get(carId)
            else:
                car = answerSlowMap.get(carId)

            # 修改车辆的planTime   当前时间片 + 最高速度 - 车辆当前速度
            # 这样能够让速度快的车辆，优先先行，慢车就会排在快车的后面
            if planTime < item[4]:
                car[1] = item[4]
            else:
                car[1] = planTime + maxSpeed - carSpeed
            answerMap.setdefault(carId, car)
            carStartCount += 1

    ####################################################以东西南北进行划分END###########################################

    ###############################################以终点进行划分#######################################################
    # # 定义系统调度时间
    # totalTIme = 600
    #
    # # 定义每个时间片调度时间
    # # step = int(totalTIme / endPointMap.keys().__len__())
    #
    # planTime = 0
    #
    # startMaxPlanTime = 0
    #
    # # 是否第一次发车
    # firstStartCar = 1
    #
    # # 已经出发的车辆
    # haveStartCar = []
    # # 获得每个分类的车辆出发时间片
    # for key, values in endPointMap.items():
    #
    #     # 把该分类下的车取出来，和以该Key作为起点的车，取出来，合并成一个新的数组
    #     # startPointCarList = startPointMap.get(key)
    #
    #     # 定义一个阈值，当小于某个值的时候，那么就将以该起点的车也一起发送
    #     startPointCarList = []
    #
    #     # tempStartPointCarList = startPointMap.get(key)
    #     # # 每个终点发送的车辆数目
    #     # thresholdValue = 30
    #     # # 进行五轮迭代发车后，就不在终点处继续发车了
    #     # if firstStartCar <= 10:
    #     #     if tempStartPointCarList != None:
    #     #         for car in tempStartPointCarList:
    #     #             if thresholdValue <= 0:
    #     #                 break
    #     #             thresholdValue = thresholdValue - 1
    #     #             startPointCarList.append(car)
    #
    #     mergeCarList = values + startPointCarList
    #
    #     # 将要出发的车辆列表
    #     willStartCar = []
    #
    #     # 判断该分类区间的车，是否有已经出发的车辆
    #     for item in mergeCarList:
    #         isStart = 0
    #         for startClassItem in haveStartCar:
    #             if item[0] == startClassItem:
    #                 isStart = 1
    #                 break
    #         if isStart == 0:
    #             willStartCar.append(item)
    #
    #     # 将马上要出发的车，存入发车列表
    #     for car in willStartCar:
    #         haveStartCar.append(car[0])
    #
    #     # 时间片大小进一步划分（根据驶入当前终点的车辆数，动态改变 ）  （总分片/ 总车辆 ）* 当前点车辆
    #     step = int((totalTIme / car_number) * len(values))
    #     # 太小的时间片，给一个默认值
    #     if step < 3:
    #         step = step + 2
    #     # 太大的时间片，是否也设置一个最大值呢？
    #
    #     # 第一次读取最大的出发时间
    #     if startMaxPlanTime == 0:
    #         # 设置状态位，表示第一次发车
    #         firstStartCar = 1
    #         for item in values:
    #             if item[4] > startMaxPlanTime:
    #                 startMaxPlanTime = item[4]
    #         planTime = startMaxPlanTime
    #     else:
    #         # 慢慢递增
    #         firstStartCar += 1
    #
    #         # 最后一些车辆，让它们一起发车
    #         if firstStartCar <= int(0.9 * endPointMap.keys().__len__()):
    #             planTime += step
    #
    #     # planC 快车先行
    #     # 得到所有车的速度数组
    #     speedArray = []
    #     maxSpeed = 0
    #     for item in willStartCar:
    #         carSpeed = item[3]
    #         flag = 0
    #         for tempSpeed in speedArray:
    #             if tempSpeed == carSpeed:
    #                 flag = 1
    #         if flag == 0:
    #             # 得到最高速度
    #             if carSpeed > maxSpeed:
    #                 maxSpeed = carSpeed
    #             speedArray.append(carSpeed)
    #
    #     speedArray = sorted(speedArray)
    #
    #     # 将车辆按速度从小到大排序
    #     tempWillStartCar = []
    #     for tempCarSpeed in speedArray:
    #         for item in willStartCar:
    #             carSpeed = item[3]
    #             if carSpeed == tempCarSpeed:
    #                 tempWillStartCar.append(item)
    #
    #     willStartCar = tempWillStartCar
    #
    #     halfMaxSpeed = int( maxSpeed/ 2)
    #
    #     halfCount = int((len(willStartCar)) / 2)
    #
    #     count_7_3 = int((len(willStartCar) / 7)*3)
    #     count_7_4 = int((len(willStartCar) / 7) * 4)
    #
    #     # 计数器，用于计算该分类下，出发的车辆
    #     startCarCount = 0
    #     for item in values:
    #         startCarCount += 1
    #
    #         # 得到车辆的ID
    #         carId = item[0]
    #         carSpeed = item[3]
    #
    #         # 按照速度划分
    #         # if carSpeed < halfMaxSpeed:
    #         #     car = answerHighMap.get(carId)
    #         # else:
    #         #     car = answerSlowMap.get(carId)
    #
    #         # 按出发车辆规划路线
    #         # if halfCount > startCarCount:
    #         #     # 走快速车道
    #         #     car = answerHighMap.get(carId)
    #         # else:
    #         #     # 走最少行驶车道
    #         #     car = answerSlowMap.get(carId)
    #
    #         # 设置一个阈值，当时间片快要结束的时候，所有的车，都走快速车道
    #         if firstStartCar <= int(0.1*endPointMap.keys().__len__()):
    #             car = answerNormalMap.get(carId)
    #
    #         elif firstStartCar <= int(0.5*endPointMap.keys().__len__()):
    #             if carSpeed < halfMaxSpeed:
    #                 car = answerHighMap.get(carId)
    #             else:
    #                 car = answerSlowMap.get(carId)
    #
    #         elif firstStartCar <= int(0.9*endPointMap.keys().__len__()):
    #             if carSpeed < halfMaxSpeed:
    #                 car = answerHighMap.get(carId)
    #             else:
    #                 car = answerSlowMap.get(carId)
    #         else:
    #             car = answerNormalMap.get(carId)
    #
    #
    #         # 修改车辆的planTime   当前时间片 + 最高速度 - 车辆当前速度
    #         # 这样能够让速度快的车辆，优先先行，慢车就会排在快车的后面
    #         if firstStartCar == 1:
    #             car[1] = item[4]
    #         else:
    #             car[1] = planTime + maxSpeed - carSpeed
    #         answerMap.setdefault(carId, car)
    ###############################################以终点进行划分#######################################################

    result = []
    for item in answerMap.values():
        result.append(item)

    output_txt(answerPath, result)


# to write output file
    end5 = datetime.datetime.now() - start
    print(end5)

if __name__ == "__main__":
    main()
