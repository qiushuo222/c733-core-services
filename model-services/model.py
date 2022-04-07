import torch
import torch.nn as nn

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


class Predictor():
    def __init__(self, model_weights_path):
        self.model = AutoEncoderNew()
        with open(model_weights_path, "rb") as f:
            weights = torch.load(f, map_location=torch.device('cpu'))
        self.model.load_state_dict(weights)
        self.model.eval()

    def predict(self, features):
        return self.model(torch.Tensor(features).float()).item()
