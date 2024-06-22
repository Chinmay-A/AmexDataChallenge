import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier
import utils

dataX = pd.read_csv('./out/dataX.csv')
dataY = pd.read_csv('./out/dataY.csv')

dataX = np.array(dataX)
dataY = np.array(dataY).ravel()

trainX, validateX, trainY, validateY = train_test_split(
    dataX, dataY, test_size=0.3, 
    random_state=42, shuffle=True
    )

def train_xgb_model():
    # Train an XGBoost model
    model = xgb.train(
        utils.hyperparams['xgboost']['params'],
        xgb.DMatrix(trainX, label=trainY),
        utils.hyperparams['xgboost']['num_rounds'],
    )
    train_preds = model.predict(xgb.DMatrix(trainX))
    val_preds = model.predict(xgb.DMatrix(validateX))
    train_preds = [1 if i > 0.5 else 0 for i in train_preds]
    val_preds = [1 if i > 0.5 else 0 for i in val_preds]

    train_accuracy = accuracy_score(trainY, train_preds)
    val_accuracy = accuracy_score(validateY, val_preds)
    print("-"*50)
    print(f'Model: XGBoost\nTrain-set Accuracy: {train_accuracy}\nValidation-set Accuracy: {val_accuracy}')
    print("-"*50)
    return model

def train_lgbm_model():
    # Train an LightGBM model
    model = lgb.train(
        utils.hyperparams['lightgbm']['params'],
        lgb.Dataset(trainX, label=trainY),
        utils.hyperparams['lightgbm']['num_rounds'],
    )
    train_preds = model.predict(trainX)
    val_preds = model.predict(validateX)
    train_preds = [1 if i > 0.5 else 0 for i in train_preds]
    val_preds = [1 if i > 0.5 else 0 for i in val_preds]

    train_accuracy = accuracy_score(trainY, train_preds)
    val_accuracy = accuracy_score(validateY, val_preds)
    print("-"*50)
    print(f'Model: LightGBM\nTrain-set Accuracy: {train_accuracy}\nValidation-set Accuracy: {val_accuracy}')
    print("-"*50)
    return model

def train_catboost_model():
    # Train an CatBoost model
    model = CatBoostClassifier(
        iterations=utils.hyperparams['catboost']['params']['iterations'],
        learning_rate=utils.hyperparams['catboost']['params']['learning_rate'],
        depth=utils.hyperparams['catboost']['params']['depth'],
        loss_function='Logloss',
        verbose=0
    )
    model.fit(trainX, trainY)

    train_preds = model.predict(trainX)
    val_preds = model.predict(validateX)
    train_accuracy = accuracy_score(trainY, train_preds)
    val_accuracy = accuracy_score(validateY, val_preds)
    print("-"*50)
    print(f'Model: CatBoost\nTrain-set Accuracy: {train_accuracy}\nValidation-set Accuracy: {val_accuracy}')
    print("-"*50)
    return model

def train_and_save_models():
    model = train_xgb_model()
    model.save_model('./out/xgb_model.json')

    model = train_lgbm_model()
    model.save_model('./out/lgbm_model.json')
    
    model = train_catboost_model()
    model.save_model('./out/catboost_model.json')

    print('Models saved successfully!')

train_and_save_models()