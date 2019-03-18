import logging
import sys
# to read input file
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

def output_txt(file_address, answer):
    with open(file_address, "w") as f:
        f.writelines("#(carId,StartTime,RoadId...)")
        f.writelines("\n")
        for j in answer:
            datastr=str(j)
            datastr=datastr.replace("[", "(")
            datastr=datastr.replace("]", ")")
            f.writelines(datastr)
            f.writelines("\n")

shortest_distance = {}
# 用Dijkstra's Algorithm算法，计算出最短路径
def Dijkstra(points, graph, start, end):
    # 最短距离字典
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

    shortest_distance[str(start) + '-' + str(end)] = roads

    return shortest_distance


logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

car = []
road = []
cross = []
answerPath = ""
def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    global  car
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

    cross_adjacency_matrix = np.ones((cross_number+1, cross_number+1))
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
                                if road[r][6] == 0 and road[r][5] == cross[i][0]:
                                    continue
                                else:
                                    cross_adjacency_matrix[i+1][x+1] = road[r][1]   # 获得路口之间距离


    # print(cross_adjacency_matrix)
    # cam = pd.DataFrame(cross_adjacency_matrix)
    # cam.to_csv('cam.csv')

    map = cross_adjacency_matrix
    for i in range(cross_number):
        for j in range(cross_number):
            Dijkstra(cross_number, map, i+1, j+1)# 从小到大


    # 路口->道路的字典
    cross_road = {}
    for i in range(road_number):
        if road[i][6] == 1:
            cross_road[str(road[i][4]) + '-' + str(road[i][5])] = road[i][0]
            cross_road[str(road[i][5]) + '-' + str(road[i][4])] = road[i][0]
        else:
            cross_road[str(road[i][4]) + '-' + str(road[i][5])] = road[i][0]

    answer = []
    # 生成每辆车的最短路径
    for i in range(car_number):
        every_answer = []
        every_answer.append(car[i][0])
        every_answer.append(car[i][4])  # 先处理成默认发车时间
        walk = shortest_distance[str(car[i][1]) + '-' + str(car[i][2])]
        for j in range(len(walk) - 1):
            every_answer.append(cross_road[str(walk[j]) + '-' + str(walk[j + 1])])
        answer.append(every_answer)

    # 定义字典，用于存储每个车的行驶路径
    answerMap = {}
    for item in answer:
        answerMap.setdefault(item[0], item)

    # 定义所有车辆起点数组
    carStartingPoint = []
    for i in range(car_number):
        # 定义标志位，判断是否包含该元素
        tag = 0
        for j in range(len(carStartingPoint)):
            if car[i][2] == carStartingPoint[j]:
                tag = 1
                break
        if tag == 0:
            carStartingPoint.append(car[i][2])

    # 定义Map，存储相同起点的车辆， key：起点   value：该起点的所有车辆
    startintPointMap = {};
    for i in range(len(carStartingPoint)):
        tempCarInfoArray = []
        for j in range(car_number):
            if carStartingPoint[i] == car[j][2]:
                tempCarInfoArray.append(car[j])
        startintPointMap.setdefault(carStartingPoint[i], tempCarInfoArray)

    # 定义系统调度时间
    totalTIme = 790

    # 定义每个时间片调度时间
    step = int(totalTIme / startintPointMap.keys().__len__())

    planTime = 0
    startMaxPlanTime = 0

    # 获得每个分类的车辆出发时间片
    for key, values in startintPointMap.items():
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
        #
        # for item in values:
        #     # 得到车辆的ID
        #     carId = item[0]
        #     car = answerMap.get(carId)
        #     # 修改车辆的planTime
        #     planTime = planTime + itemPlanTime
        #     car[1] = planTime
        #     answerMap.setdefault(carId, car)

        # planC 快车先行
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
                speedArray.append(carSpeed)

        for speed in speedArray:
            if speed > maxSpeed:
                maxSpeed = speed
        for item in values:
            # 得到车辆的ID
            carId = item[0]
            carSpeed = item[3]
            car = answerMap.get(carId)
            # 修改车辆的planTime   当前时间片 + 最高速度 - 车辆当前速度
            # 这样能够让速度快的车辆，优先先行，慢车就会排在快车的后面
            car[1] = planTime + maxSpeed - carSpeed
            answerMap.setdefault(carId, car)


    result = []
    for item in answerMap.values():
        result.append(item)

    output_txt(answerPath, result)

# to write output file


if __name__ == "__main__":
    main()