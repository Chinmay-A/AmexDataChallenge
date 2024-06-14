import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
import xgboost as xgb
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import accuracy_score

class xgboostModel:
    
    def __init__(self,train_data) -> None:
        # self.relevant_features=['winner_id','team_count_50runs_last15','team_winp_last5','team1only_avg_runs_last15','team1_winp_team2_last15','ground_avg_runs_last15']
        # self.train_data=train_data[self.relevant_features]
        self.train_data=train_data

        self.hyperparameters = {
            'n_estimators': 1000,
            'max_depth': 6,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'learning_rate': 0.02,
            'eta': 0.015,
        }
        
        self.train, self.validate=train_test_split(self.train_data,train_size=0.75,random_state=21)
        
        self.trainY=self.train['winners']
        self.trainX=self.train.drop('winners',axis=1)

        self.testY=self.validate['winners']
        self.testX=self.validate.drop('winners',axis=1)

        print("Init successful")
    
    @staticmethod
    def getlabel(dataA,dataB):
        if(dataA==dataB):
            return 1
        return 0
    def train_model(self):

        # print("here")
        xgb_params = {
            'n_estimators': self.hyperparameters['n_estimators'],
            'objective':'binary:logistic',
            'max_depth':self.hyperparameters['max_depth'],
            'eta':self.hyperparameters['eta'],
            'random_state':45,
            'subsample': self.hyperparameters['subsample'],
            'colsample_bytree':self.hyperparameters['colsample_bytree']
        }
        n_round = 500

        self.train_matrix = xgb.DMatrix(self.trainX, label=self.trainY)
        self.validate_matrix = xgb.DMatrix(self.testX, label=self.testY)
        watchlist = [(self.validate_matrix, 'validation')]
        self.bst = xgb.train(xgb_params, self.train_matrix, n_round, evals=watchlist, early_stopping_rounds=50, verbose_eval=500)
        
    def predict(self, data):
        data_matrix = xgb.DMatrix(self.testX)
        preds = self.bst.predict(data_matrix, iteration_range=(0, self.bst.best_iteration + 1))
        return preds
    
    def evaluate(self):
        preds = self.predict(self.validate_matrix)
        for i in range(len(preds)):
            if(preds[i]>=0.5):
                preds[i]=1
            else:
                preds[i]=0
        accuracy = accuracy_score(self.testY, preds)
        print(f'Accuracy: {accuracy}')
        return accuracy
