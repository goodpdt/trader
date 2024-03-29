import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

import keras
from keras.models import load_model

from agent.agent import Agent
from functions import *
import sys

if len(sys.argv) != 3:
	print("Usage: python evaluate.py [stock] [model]")
	exit()

stock_name, model_name = sys.argv[1], sys.argv[2]
model = load_model("models/" + model_name)
window_size = model.layers[0].input.shape.as_list()[1]
print("windows size = ",window_size)

agent = Agent(window_size, False, model_name) #true false!

data = getStockDataVec(stock_name)
#print(data)
l = len(data) - 1
print("len(data) = ",l)
batch_size = 32


state = getState(data, 0, window_size + 1)
total_profit = 0
agent.inventory = []

for t in range(l):
	action = agent.act(state)
	#print(action)
	# sit
	next_state = getState(data, t + 1, window_size + 1)
	reward = 0
	if action == 1: # buy
		agent.inventory.append(data[t])
		print("Buy: " + formatPrice(data[t]))

	elif action == 2 and len(agent.inventory) > 0: # sell
		#print("inventory = ",len(agent.inventory))
		bought_price = agent.inventory.pop(0)
		#print("bought_price = ",bought_price)
		reward = max(data[t] - bought_price, 0)
		total_profit += data[t] - bought_price
		print("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
		#print("inventory = ",len(agent.inventory))
	else:
		print("sit: ",action)

	done = True if t == l - 1 else False
	agent.memory.append((state, action, reward, next_state, done))
	
	state = next_state

	if done:
		print("\ncheck inventory")
		print("inventory = ",len(agent.inventory))
		print("final price: " + formatPrice(data[t]))
		print("All Sell")
		while(len(agent.inventory)>0):
			bought_price = agent.inventory.pop(0)
			total_profit += data[t] - bought_price
			print("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))

		if(len(agent.inventory)==0):
			print("All Sell done")
			print("--------------------------------")
			print(stock_name + " Total Profit: " + formatPrice(total_profit))
			print("--------------------------------")
		else:
			print("some error")