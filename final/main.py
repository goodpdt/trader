import matplotlib.pyplot as plt
import subprocess
import pandas as pd
import csv

#run evaluate2.py
def call(stock_name, model, money):
    print("python evaluate2.py {} {} {}".format(stock_name, model, money))
    #subprocess.call("python3 evaluate2.py {} {} {}".format(stock_name, model, money), shell=True)
    subprocess.call("python evaluate2.py {} {} {}".format(stock_name, model, money), shell=True)

months = ""
with open("./data/percentage.csv") as f: #input data
    months = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    mon = 1
    for row in months:
        #print(row)
        if mon is not 1:
            remain_total_money = 0
            for i in range(len(row)):
                if i%2 == 0:
                    with open("./data/remain_money/_" + row[i] + ".TW.txt", 'r') as g:
                        remain_money = g.read()
                        remain_total_money += float(remain_money)
            #print(remain_total_money)
            #break
        else:
            remain_total_money = 100000
            first_month = False

            #split stock into month data
            '''for i in range(len(row)):
                if i%2 == 0:
                    df = pd.read_excel("./data/test/_" + row[i] + ".TW.xlsx")
                    for j in range(1,13):
                        print(j)
                        print(df[(df.iloc[:,0].dt.month == j) & (df.iloc[:,0].dt.year != 2004)])
                        df1 = df[(df.iloc[:,0].dt.month == j) & (df.iloc[:,0].dt.year != 2004)]
                        df1.to_excel("./data/test/cut/_"+ row[i] + ".TW-" + str(j) + ".xlsx", index=False)'''
            #break

        for i in range(len(row)):
            #print(row[i])
            if i%2 == 0:
                print(row[i+1])
                money = float(remain_total_money) * float(row[i+1])
                call("_"+row[i]+".TW-"+str(mon), "model_"+row[i], money)
                
        mon += 1

#total asset calculate
total = []
with open("./data/percentage.csv") as f:
    months = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    mon = 0
    for row in months:
        for i in range(len(row)):
            if i%2 == 0:
                with open("./data/stock_total_value/_" + row[i] + ".TW.txt", 'r') as g:
                    values = g.read()
                    if i == 0:
                        total.append(float(values.split(",")[mon]))
                    else:
                        total[mon] += float(values.split(",")[mon])
        mon += 1
print(total)

#draw
y = total
x = []
for i in range(1,len(total)+1):
    x.append(i)
plt.plot(x,y,'k')
plt.ylabel('Money')
plt.xlabel('Month')

plt.savefig('result.png')
