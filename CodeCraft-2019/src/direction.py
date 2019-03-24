import math

car = [[10001, 18, 73, 4, 88],
[10002, 65, 20, 8, 13],
[10003, 75, 10, 4, 1],
[10004, 66, 11, 6, 99],
[10005, 98, 1, 6, 44],
[10006, 37, 81, 8, 93]]



def direction(x,y,cross_number):
    width=math.sqrt(cross_number)

    if x-int(x/width)*width == 0:
        x_du = x-int(x/width)*width + width
    else:
        x_du = x - int(x / width) * width
    if y-int(y/width)*width == 0:
        y_du = y-int(y/width)*width + width
    else:
        y_du = y - int(y / width) * width
    if int(y/width)-width/2 < int(x/width) < int(y/width)+width/2:
        if x_du <= y_du:
            print("北")
        else:
            print("南")
    else:
        if x <= y:
            print("东")
        else:
            print("西")

for item in car:
    direction(item[1],item[2],100)