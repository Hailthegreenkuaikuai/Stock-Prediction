"""
This module contains preprocessing utilities for data preparation.

1. Split the dataset into training and testing sets. 
2. Create sequences windows
3. Create dataloader 
"""
import numpy as np
import pandas as pd
import torch

def split_data(data, split_ratio, n_past):
    train_size = int(len(data) * split_ratio)
    train_data = data[:train_size]
    val_data = data[train_size:]
    X_train, Y_train = create_sequences(train_data, n_past)
    X_val, Y_val = create_sequences(val_data, n_past)

    return X_train, Y_train, X_val, Y_val

def create_sequences(data, n_past):
    X, Y = [], []
    length = len(data)
    for i in range(length - (n_past + 5)):
        X.append(data[i:i + n_past])
        Y.append(data[i + n_past:i + n_past + 5][:, 4])
    return torch.Tensor(np.array(X)), torch.Tensor(np.array(Y))

df = pd.read_csv('./data/es1.csv')
data = df[['Open', 'High', 'Low', 'Close', 'Volume']].values
X_train, Y_train, X_val, Y_val = split_data(data, 0.8, 20)
batch_size = 32

train_set = torch.utils.data.TensorDataset(X_train, Y_train)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)

val_set = torch.utils.data.TensorDataset(X_val, Y_val)
val_loader = torch.utils.data.DataLoader(val_set, batch_size=batch_size, shuffle=False)