## Running the Code

```
mkdir models
python train.py ^GSPC 10 1000
python train2.py ^GSPC 10 1000
```

Then when training finishes (minimum 200 episodes for results):
```
python evaluate.py ^GSPC_2011 model_ep1000
python evaluate2.py ^GSPC_2011 model_ep1000 2000
```

## dynamic invest for many company

In dynamic Folder, delete all data in data/remain_money, data/remain_stocks and data/stock_total_value before running the code.
check input:
    1.data/percentage.csv
    2.data/test/target.TW.xlsx
    3.model_company
```
python main.py
```

## Reference

[Q-Trader](https://github.com/edwardhdlu/q-trader)

