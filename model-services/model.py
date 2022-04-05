import numpy as np
import torch
import torch.nn as nn
import pickle

class AutoEncoderNew(nn.Module):
    def __init__(self):
        super(AutoEncoderNew, self).__init__()
        self.name = "AE"
        self.encoder = nn.Sequential(
            nn.Linear(5, 4), 
            nn.ReLU(),
            nn.Linear(4, 3), 
            nn.ReLU(),
            nn.Linear(3, 2), 
            nn.ReLU(),
            nn.Linear(2, 1), 
        )
    def forward(self, x):
        x = self.encoder(x)
        return x

def load_model(model, path):
    # load
    with open(path, 'rb') as f:
        model = pickle.load(f)
        return model

def model_mock(features):
    model = AutoEncoderNew()
    model = load_model(model, 'val_best.pkl')
    pred = model(torch.Tensor(features).float())
    return pred
