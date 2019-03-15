import pandas as pd
import numpy as np

print("hahahaha")
print("hahahaha")
print("hahahaha")
print("hahahaha")

# def input_txt(file_address):
#     with open(file_address, "r") as f:
#         str = f.read()
#         str = str.replace("(", "")
#         str = str.replace(")", "")
#         str = str.replace("\n", ",")
#         str = str.lstrip('#qwertyuiopasdfghjklzxcvbnm,QWERTYUIOPASDFGHJKLZXCVBNM')
#
#     arr = str.split(',')
#     Arr = np.array(arr)
#     Arr = Arr.reshape(-1, 5)
#     return Arr
#
#
# car = input_txt("../config/car.txt")
# road = input_txt("../config/road.txt")
# cross = input_txt("../config/cross.txt")

#总路口数
cross_number = len(cross)

cross_adjacency_matrix = np.zeros((cross_number, cross_number))
#构建路口的邻接矩阵
for i in range(cross_number):
    for j in range(1,5):
        if cross[i][j] == -1:
            continue
        for x in range(cross_number):
            for y in range(1, 5):
                if cross[i][j] == cross[x][y]:
                    cross_adjacency_matrix[i][x] = 1

print("hahahaha")
print(cross_adjacency_matrix)

