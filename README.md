## Running the Code

```
mkdir models
python train.py ^GSPC 10 1000
```

Then when training finishes (minimum 200 episodes for results):
```
python evaluate.py ^GSPC_2011 model_ep1000
```

## Reference

[Q-Trader](https://github.com/edwardhdlu/q-trader)

