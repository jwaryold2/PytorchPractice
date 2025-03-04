import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):

    def __init__(self, in_features = 10, h1 = 8, h2 = 7, h3 = 4, h4 = 6, out_features = 2):
        super().__init__()
        self.fc1 = nn.Linear(in_features, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.fc3 = nn.Dropout(.3)
        self.fc4 = nn.Linear(h2, h3)
        self.out = nn.Linear(h2, out_features)

    def forward(self, x):
        x = F.sigmoid(self.fc1(x))
        x = F.sigmoid(self.fc2(x))
        x = self.fc3(x)
        x = self.fc4(x)
        return F.sigmoid(self.out(x))


model = Model()

test_df = pd.read_csv('test.csv')
train_df = pd.read_csv('train.csv')

#Seperate features and Label
X_test = test_df.drop("id", axis =1)
X_test = X_test.drop("day", axis =1)
X_test=X_test.values
X_test = torch.FloatTensor(X_test)


X_train = train_df.drop("rainfall", axis = 1)
X_train = X_train.drop("id", axis = 1)
X_train = X_train.drop("day", axis = 1)
y_train = train_df["rainfall"]


print(X_train)
#turn into numpy arrays
X_train = X_train.values
y_train = y_train.values
#Tunr into tensors
X_train = torch.FloatTensor(X_train)
y_train = torch.LongTensor(y_train)

lossfn = nn.CrossEntropyLoss()
optim = torch.optim.Adam(model.parameters())

epochs = 35000

for i in range(epochs):
    y_p = model.forward(X_train)
    loss = lossfn(y_p, y_train)

    optim.zero_grad()
    loss.backward()
    optim.step()

    if i % 10 == 0:
        print(f"epoch {i} and loss of {loss}")

y_pred =[]
with torch.no_grad():
    for i, data in enumerate(X_test):
        y_vl = model.forward(data)
        y_pred.append(y_vl.argmax().item())


result = pd.DataFrame({"id": test_df.id, "rainfall": y_pred})
result.to_csv('result1.csv', index=False)