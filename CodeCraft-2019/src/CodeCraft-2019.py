import logging
import sys
# to read input file

import numpy as np


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
def Dijkstra(points, graph, start, end, dictionary,_cross):
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
        roads.append(_cross[road[len]-1][0])
        len -= 1
    # print(str(start+1)+" 到 "+str(end+1))
    # print("最短距离：", dis[end],end=" ")
    # print("最短路径：", roads)
    dictionary[str(_cross[start-1][0]) + '-' + str(_cross[end-1][0])] = roads


# 固定map图
def map(cross_number, matrix, dictionary,_cross):
    for i in range(cross_number):
        for j in range(cross_number):
            Dijkstra(cross_number, matrix, i + 1, j + 1, dictionary,_cross)  # 普通权重


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


def generating_path(car, path, node, cross_road, count_road_frequency,count_cross_frequency):  # node:生成车辆的节点路径
    for i in car:
        every_answer = [i[0], i[4]]
        walk = node[str(i[1]) + '-' + str(i[2])]
        for j in range(len(walk) - 1):
            # count_cross_frequency[walk[j]] += 1
            # count_road_frequency[(cross_road[str(walk[j]) + '-' + str(walk[j + 1])])] += 1
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
def direction(cross_number, car):
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
        if x-(width*(3.6)*width) < y < x+(width*(3.6)*width):
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

    # cross_adjacency_matrix = np.ones((cross_number + 1, cross_number + 1))
    # cross_adjacency_matrix = float('inf') * cross_adjacency_matrix
    cross_adjacency_high_speed = np.ones((cross_number + 1, cross_number + 1))
    cross_adjacency_high_speed = float('inf') * cross_adjacency_high_speed
    cross_adjacency_slow_speed = np.ones((cross_number + 1, cross_number + 1))
    cross_adjacency_slow_speed = float('inf') * cross_adjacency_slow_speed
    # cross_adjacency_infrequent = np.ones((cross_number + 1, cross_number + 1))
    # cross_adjacency_infrequent = float('inf') * cross_adjacency_infrequent
    # cross_adjacency_wide_road = np.ones((cross_number + 1, cross_number + 1))
    # cross_adjacency_wide_road = float('inf') * cross_adjacency_wide_road

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
                                    # cross_adjacency_matrix[i + 1][x + 1] = (
                                    #         road[r][1] / (0.95 * road[r][2] * (road[r][3])))  # 获得路口之间距离
                                    cross_adjacency_high_speed[i + 1][x + 1] = (
                                            10 / (1.5 * road[r][2] * (road[r][3])))# 速度块
                                    cross_adjacency_slow_speed[i + 1][x + 1] = (road[r][2] / (road[r][3]))# 速度慢
                                    # cross_adjacency_wide_road[i + 1][x + 1] = 10/road[r][3]

    # 重新评估权重2019-3-18
    # print(cross_adjacency_wide_road)
    # print(cross_adjacency_matrix)
    # print(cross_adjacency_infrequent)
    # cam = pd.DataFrame(cross_adjacency_matrix)
    # cam.to_csv('cam.csv')

    end1 = datetime.datetime.now()-start
    print(end1)#0.282849s

    # 生成经过cross的路线

    # # 最短距离节点路径字典
    # shortest_distance = Manager().dict()
    # 速度最快节点路径字典
    high_speed = Manager().dict()
    # 速度最慢节点路径字典
    slow_speed = Manager().dict()
    # # 频率低节点路径字典
    # low_frequency = Manager().dict()
    # 道路宽的路径字典
    wide_road = {}

    # p1 = Process(target=map,args=(cross_number, cross_adjacency_matrix,shortest_distance,cross))#普通路线
    p2 = Process(target=map,args=(cross_number, cross_adjacency_high_speed, high_speed,cross))  # 速度最快路线
    p3 = Process(target=map,args=(cross_number, cross_adjacency_slow_speed, slow_speed,cross))  # 速度最慢路线
    # p1.start()
    p2.start()
    p3.start()

    # p1.join()
    p2.join()
    p3.join()
    # map(cross_number, cross_adjacency_wide_road, wide_road)  # 路最的宽路线
    # print(shortest_distance)
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
    # generating_path(car, answer, shortest_distance, cross_road,
    #                 count_road_frequency,count_cross_frequency)#普通路线
    generating_path(car, answer_high_speed, high_speed, cross_road,
                    count_road_frequency,count_cross_frequency)  # 速度最快路线
    generating_path(car, answer_slow_speed, slow_speed, cross_road,
                    count_road_frequency,count_cross_frequency)  # 速度最慢路线
    # generating_path(car, answer_wide_road, wide_road, cross_road,
    #                 count_road_frequency, count_cross_frequency)  # 道路宽路线

    end3 = datetime.datetime.now() - start
    print(end3)#2.03.45

    ###################################方向车辆################

    # key：东西，南北    value：东西南北车辆Array
    directionMap = direction(cross_number, car)

    ###################################方向车辆################



    ################################频率最低路线生成###########################################
    # for i in range(int(road_number / 3)):  # 设置：取消道路行驶权占总道路的比例
    #     max_frequency_road = 0
    #     index_frequency_road = 0
    #     for i in range(len(count_road_frequency)):
    #         if count_road_frequency[i] < float('inf'):
    #             if count_road_frequency[i] > max_frequency_road:
    #                 max_frequency_road = count_road_frequency[i]
    #                 index_frequency_road = i
    #     count_road_frequency[index_frequency_road] = 999999
    # # print(count_road_frequency)
    #
    # for i in range(cross_number):
    #     for j in range(1, 5):
    #         if cross[i][j] == -1:
    #             continue
    #         for x in range(cross_number):
    #             for y in range(1, 5):
    #                 if cross[i][j] == cross[x][y]:  # 找出相邻路口
    #                     for r in range(road_number):
    #                         if road[r][0] == cross[i][j] and i != x:
    #                             if road[r][6] == 0 and road[r][5] == cross[i][0]:
    #                                 continue
    #                             else:
    #                                 cross_adjacency_infrequent[i + 1][x + 1] = count_road_frequency[r]/road[r][3] # 行驶次数最少的路
    #
    # # 低频路线，取消频率过高路线的行驶权
    # # for item in cross_adjacency_infrequent
    # #     if item >= cross_adjacency_infrequent.reshape(1,-1)
    #
    # map(cross_number, cross_adjacency_infrequent, low_frequency)  # 频率低的路线
    # #print(count_cross_frequency)
    # generating_path(car_number, answer_low_frequency, low_frequency, cross_road
    #                 , count_road_frequency, count_cross_frequency)  # 频率低的路线
    #
    # end4 = datetime.datetime.now() - start
    # print(end4)
    #################################频率最低路线生成################################################

    # 定义答案Map
    answerMap = {}

    # 定义字典，用于存储每个车的高速行驶路径
    answerHighMap = {}
    for item in answer_high_speed:
        answerHighMap.setdefault(item[0], item)

    # 定义字典，用于存储每个车的低速行驶路径
    answerSlowMap = {}
    for item in answer_slow_speed:
        answerSlowMap.setdefault(item[0], item)

    # 定义字典，用于存储道路的长度
    roadMap = {}
    for roadItem in road:
        roadMap.setdefault(roadItem[0], roadItem[1])

    # 定义字典，用于存储车辆  key：carId   value:  car
    carMap = {}
    for carItem in car:
        carMap.setdefault(carItem[0], carItem)

    ###################################################以东西南北进行划分##############################################

    planTime = 0
    # 是否第一次发车
    firstStartCar = 0

    # 记录外层循环次数
    tempCount = 0

    for key, values in directionMap.items():
        # 对所有南北  和 东西的车辆进行按距离分类

        # # 定义所有车辆距离字典
        # carDistance = {}
        # for item in values:
        #     # 通过carId获取到车辆的路径
        #     answerNormalDis = answerNormalMap.get(item[0])
        #     sumRoadLen = 0
        #     for i in range(2, len(answerNormalDis)):
        #         roadLen = roadMap.get(answerNormalDis[i])
        #         sumRoadLen += roadLen
        #     # 设置每辆车的距离长度
        #     carDistance.setdefault(item[0], sumRoadLen)
        #
        # # 得到所有的距离长度
        # carDistanceArray = carDistance.values()
        #
        # # 数组去重
        # carDistanceArray = list(set(carDistanceArray))
        #
        # # 数组排序
        # # carDistanceArray = sorted(carDistanceArray, reverse=True)
        # carDistanceArray = sorted(carDistanceArray)
        #
        # # 定义数组，用于记录距离从小到大的车辆
        # sortCarDistanceArray = []
        # for carDistanceItem in carDistanceArray:
        #     for key, values in carDistance.items():
        #         if values == carDistanceItem:
        #             tempCar = carMap.get(key)
        #             sortCarDistanceArray.append(tempCar)

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

        halfMaxSpeed = int( maxSpeed/ 2)
        halfMaxSpeed_8_3 = int(maxSpeed * (3/8))
        halfMaxSpeed_8_5 = int(maxSpeed * (5/8))

        # 车辆发车计数器
        carStartCount = 1

        if tempCount == 0:
            shardCount = 130
        else:
            shardCount = 120

        # if planTime > 0:
        #     planTime += 38

        #按照速度划分
        for item in values:

            if carStartCount % shardCount == 0:
                # 最后的车辆，同时发车
                if tempCount == 0:
                    if carStartCount <= int(0.15*values.__len__()):
                        planTime += 3.5
                    else:
                        planTime += 4.5

                elif tempCount >= 1:
                    if carStartCount <= int(0.8*values.__len__()):
                        planTime += 4
                    elif carStartCount <= int(0.9*values.__len__()):
                        planTime += 3

            # 得到车辆的ID
            carId = item[0]
            carSpeed = item[3]

            # if carSpeed < halfMaxSpeed:
            #     car = answerHighMap.get(carId)
            # else:
            #     car = answerSlowMap.get(carId)

            if carStartCount < int(0.2*values.__len__()):
                car = answerHighMap.get(carId)
            elif carStartCount < int(0.8*values.__len__()):
                # 按照速度划分
                if carSpeed == 4 or carSpeed == 6:
                    if carStartCount % 7 == 0:
                        car = answerHighMap.get(carId)
                    else:
                        car = answerHighMap.get(carId)
                else:
                    if carStartCount % 7 == 0:
                        car = answerHighMap.get(carId)
                    else:
                        car = answerSlowMap.get(carId)
            else:
                car = answerHighMap.get(carId)

            # 修改车辆的planTime   当前时间片 + 最高速度 - 车辆当前速度
            # 这样能够让速度快的车辆，优先先行，慢车就会排在快车的后面
            if planTime < item[4]:
                car[1] = item[4]
            else:
                car[1] = int(planTime + maxSpeed - carSpeed)
            answerMap.setdefault(carId, car)
            carStartCount += 1

        tempCount +=1
    ####################################################以东西南北进行划分END###########################################

    result = []
    for item in answerMap.values():
        result.append(item)

    output_txt(answerPath, result)


# to write output file
    end5 = datetime.datetime.now() - start
    print(end5)
    print(len(directionMap['NorthAndSouth']))
    print(len(directionMap['EastAndWest']))

if __name__ == "__main__":
    main()
