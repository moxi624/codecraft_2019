import pandas as pd
import numpy as np


with open("../config/car.txt","r") as f:
    str = f.read()
    str = str.replace("(", "")
    str = str.replace(")", "")
    str = str.lstrip('#qwertyuiopasdfghjklzxcvbnm,QWERTYUIOPASDFGHJKLZXCVBNM')


car = pd.DataFrame(str)
