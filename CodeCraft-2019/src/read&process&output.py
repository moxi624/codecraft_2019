import pandas as pd
import numpy as np


with open("../config/car.txt","r") as f:
    str = f.read()
    str = str.replace("(", "")
    str = str.replace(")", "")
    str = str.replace("\n", ",")
    str = str.lstrip('#qwertyuiopasdfghjklzxcvbnm,QWERTYUIOPASDFGHJKLZXCVBNM')

arr = str.split(',')
car = np.array(arr)
car = car.reshape(-1,5)
print(car)
