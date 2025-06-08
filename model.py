import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if(torch.cuda.is_available()):
    device = "cuda:0"
else:
    device = "cpu"

fileList = ["msft", "nvda", "tsla"]

"""
for file in fileList:
    print("norm_" + file + ".csv")
"""
data_norm = pd.read_csv("stock/norm_nvda.csv")
data = pd.read_csv("stock/nvda.csv")

data['Time'] = pd.to_datetime(data['Time'], unit='s')
data_norm['Time'] = pd.to_datetime(data_norm['Time'], unit='s')

plt.plot(data_norm['Time'], data_norm['Close'], label='Normalized Close Price', color='blue')
#plt.plot(data['Time'], data['Close'], label='Close Price', color='orange')
plt.show()




