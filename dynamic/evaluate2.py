import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#-1 = close GPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import keras
from keras.models import load_model

from agent.agent import Agent
from functions2 import *
import sys
import pandas as pd

if len(sys.argv) != 4:
    print("Usage: python evaluate.py [stock] [model] [money]")
    exit()

stock_name_dash, model_name, money = sys.argv[1], sys.argv[2], float(sys.argv[3])
stock_name = stock_name_dash.split("-")[0]
model = load_model("models2/" + model_name)
window_size = model.layers[0].input.shape.as_list()[1]
print("windows size = ",window_size)
print("Money = ",money)

#taiwan stock
#0.1425% handling fee
#0.3% tax
fee = 0
tax = 0

buy_num = 0
sell_num = 0
sit_num = 0

agent = Agent(window_size, False, model_name) #true false!

data = getStockDataVec("test/cut/" + stock_name_dash)
#print(data)
l = len(data) - 1
print("len(data) = ",l)
batch_size = 32


state = getState(data, 0, window_size + 1)
total_profit = 0
agent.inventory = []
try:
    df = pd.read_csv(r"./data/remain_stocks/" + stock_name + ".csv")
    stock_prices = df.to_numpy()
    for i in stock_prices[0:]:
        #print(i[0])
        agent.inventory.append(i[0])
except:
    pass
print(agent.inventory)

#money
for t in range(l):
    action = agent.act(state)
    #print(action)
    # sit
    next_state = getState(data, t + 1, window_size + 1)	
    reward = 0
    #print("data[t] is ",data[t])
    if action == 1 and money > data[t]: # buy
        buy_num+=1
        agent.inventory.append(data[t])
        print("Buy: " + formatPrice(data[t]))
        money = money - data[t] - 0.001425*data[t]

        reward = -data[t]*0.004425

        fee += 0.001425*data[t]
        print("Remaining money: ",money)

    elif action == 2 and len(agent.inventory) > 0: # sell
        sell_num+=1
        #print("inventory = ",len(agent.inventory))
        bought_price = agent.inventory.pop(0)
        #print("bought_price = ",bought_price)

        #reward = max(data[t] - bought_price, 0)
        reward = data[t] - 0.004425*data[t] - 1.001425*bought_price
		
        total_profit += data[t] - bought_price
        print("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
        money = money + data[t] - 0.004425*data[t]
        fee += 0.001425*data[t]
        tax += 0.003*data[t]
        print("Remaining money: ",money)
        #print("inventory = ",len(agent.inventory))
    else:
        print("sit: ",action)
        sit_num+=1

    done = True if t == l - 1 else False
    agent.memory.append((state, action, reward, next_state, done))
	
    state = next_state

    if done:
        '''print("\ncheck inventory")
        print("len inventory = ",len(agent.inventory))
        print("inventory = ", agent.inventory)
        print(type(agent.inventory))
        print("final price: " + formatPrice(data[t]))
        print("All Sell")'''
        df = pd.DataFrame(agent.inventory)
        df.to_csv("./data/remain_stocks/" + stock_name + ".csv", sep=',',index=False)
        with open("./data/remain_money/" + stock_name + ".txt", 'w') as a:
            a.write(str(money)+"\n")

        while(len(agent.inventory)>0):
            bought_price = agent.inventory.pop(0)
            total_profit += data[t] - bought_price
            #print("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
            money = money + data[t] - 0.004425*data[t]
            fee += 0.001425*data[t]
            tax += 0.003*data[t]
            #print("Remaining money: ",money)

        if(len(agent.inventory)==0):
            '''print("--------------------------------")
            print("All Sell done")
            print("Buy ",buy_num," times")
            print("Sell ",sell_num," times")
            print("Sit ",sit_num," times")
            print("--------------------------------")
            print(stock_name + " Total Profit:" + formatPrice(total_profit))
            print('{:20}'.format("Handling fee:"), fee)
            print('{:20}'.format("Tax:"), tax)
            print('{:20}'.format("Remaining money:"), money)
            #df1 = pd.DataFrame(money)
            print("--------------------------------")'''
            try:
                with open("./data/stock_total_value/" + stock_name + ".txt", 'a') as f:
                    print(","+str(money))
                    f.write(str(money)+",")
                #df1.to_csv("./data/stock_total_value/" + stock_name + ".csv", mode='a', header=False, index=False)
            except:
                pass
                #with open("./data/stock_total_value/" + stock_name + ".txt", 'w') as f:
                    #print(str(money))
                    #f.write(str(money))
                #df1.to_csv("./data/stock_total_value/" + stock_name + ".csv", index=False)
        
        else:
            print("some error")
