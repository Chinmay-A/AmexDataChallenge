import pandas as pd
from ensemble import Model

train = pd.read_csv('./new_dataset.csv')
train.drop(columns=['bat_above_75_a','bat_above_75_b'],inplace=True)

modelA=Model(train)

modelA.train_model()
