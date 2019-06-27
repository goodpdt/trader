import subprocess
import pandas as pd
import csv

def call(stock_name, model, money):
    print("python3 evaluate2.py {} {} {}".format(stock_name, model, money))
    subprocess.call("python3 evaluate2.py {} {} {}".format(stock_name, model, money), shell=True)

months = ""
with open("./data/percentage.csv") as f:
    months = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    first_month = True
    for row in months:
        #print(row)
        if not first_month:
            remain_total_money = 0
            for i in range(len(row)):
                if i%2 == 0:
                    with open("./data/remain_money/_" + row[i] + ".TW.txt", 'r') as f:
                        remain_money = f.read()
                        remain_total_money += float(remain_money)
            #print(remain_total_money)
            #break
        else:
            remain_total_money = 1000000
            first_month = False

        for i in range(len(row)):
            #print(row[i])
            if i%2 == 0:
                print(row[i+1])
                money = float(remain_total_money) * float(row[i+1])
                call("_"+row[i]+".TW", "model_ep10", money)
                
