answer=[[1001, 1, 501, 502, 503, 516, 506, 505, 518, 508, 509, 524],
        [1002, 1, 513, 504, 518, 508, 509, 524],
        [1003, 2, 513, 517, 507, 508, 509, 524]]

def output_txt(file_address):
    with open(file_address, "w") as f:
        f.writelines("#(carId,StartTime,RoadId...)")
        f.writelines("\n")
        for j in answer:
            datastr=str(j)
            datastr=datastr.replace("[", "(")
            datastr=datastr.replace("]", ")")
            print(datastr)
            f.writelines(datastr)
            f.writelines("\n")
output_txt("../config/answer.txt")