import pandas as pd
from try_model import xgboostModel

train = pd.read_csv('train_ready.csv')
model=xgboostModel(train)

model.train()

model.evaluate()
