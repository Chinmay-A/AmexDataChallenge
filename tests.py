from data import Data
from try_model import xgboostModel

amexdata=Data()
model=xgboostModel(amexdata.TRAIN)

model.train()

