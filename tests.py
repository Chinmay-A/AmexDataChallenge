import pandas as pd
from try_model import xgboostModel

train = pd.read_csv('train_ready.csv')
print(train.head())
model=xgboostModel(train)

model.train_model()

model.evaluate()
