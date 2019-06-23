import numpy as np
import pandas as pd
import math

# prints formatted price
def formatPrice(n):
    return ("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))

# returns the vector containing stock data from a fixed file
def getStockDataVec(key):
    vec = []
    df = pd.read_excel(r"data/" + key + ".xlsx")
    #print(df.head(15))
    num = 0 
    openP = 0
    highP = 0
    lowP = 0
    volume = 0
    for title in df:
        if "PRICE HIGH" in title:
            highP = num
        elif "PRICE LOW" in title:
            lowP = num
        elif "OPENING PRICE" in title:
            openP = num
        elif ("TURNOVER BY VOLUME" in title) and (len(title.split("-"))==2) :
            volume = num
        num+=1
            
    temp = df.iloc[:, [0, openP, highP, lowP, 1, 1, volume]]
    lines = temp.to_numpy()
    #lines = open("data/" + key + ".xlsx", "r").read().splitlines()

    for line in lines[0:]:
        vec.append(float(line[4]))

    return vec

# returns the sigmoid
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# returns an an n-day state representation ending at time t
def getState(data, t, n):
    d = t - n + 1
    block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1] # pad with t0
    res = []
    for i in range(n - 1):
        res.append(sigmoid(block[i + 1] - block[i]))

    return np.array([res])
