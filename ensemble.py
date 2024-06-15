import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler

from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

from numpy import mean
from numpy import std

from sklearn.metrics import accuracy_score

from catboost import CatBoostClassifier

class Model:
    
    def __init__(self,train_data) -> None:

        self.train_data=train_data
        
        self.train, self.validate=train_test_split(self.train_data,train_size=0.75,random_state=42)
        
        self.trainY=self.train['winner']
        self.trainX=self.train.drop('winner',axis=1)

        self.trainX.fillna(0,inplace=True)
        #print(self.trainX.head())

        self.testY=self.validate['winner']
        self.testX=self.validate.drop('winner',axis=1)
        self.testX.fillna(0,inplace=True)
        #print(self.testX.head())

        print("Init successful")
    
    
    def train_model(self):

        # self.modelGBM = GradientBoostingClassifier(n_estimators=50,max_depth=2,verbose=0)
        # self.modelGBM.fit(self.trainX, self.trainY)

        self.modelGBMA = CatBoostClassifier(n_estimators=5,max_depth=8,bagging_temperature=1,learning_rate=0.8)
        self.modelGBMA.fit(self.trainX, self.trainY)

        # self.modelGBMB = GradientBoostingClassifier(n_estimators=80,max_depth=4,verbose=0)
        # self.modelGBMB.fit(self.trainX, self.trainY)

        
        #self.catmodel = CatBoostClassifier(verbose=0, n_estimators=40)
        #self.catmodel.fit(self.trainX, self.trainY)

        # model = CatBoostClassifier(verbose=0, n_estimators=100)
        # cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        # n_scores = cross_val_score(self.modelGBMA, self.trainX,self.trainY, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')

        #print('Accuracy: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))

        self.evaluate()

        
    def predict(self):
        
        #preds = self.modelGBM.predict(self.testX)
        predsA = self.modelGBMA.predict(self.testX)
        # predsB = self.modelGBMB.predict(self.testX)

        # predsC=self.catmodel.predict(self.testX)

        # net_pred=[]

        # for i in range(len(predsC)):

        #     net_pred.append((predsA[i]+predsC[i])/2)
        
        return predsA
    
    def evaluate(self):
        preds = self.predict()
        preds_linear=[]
        for pred in preds:
            #print(pred)
            if(pred>0.5):
                preds_linear.append(1)
            else:
                preds_linear.append(0)
        accuracy = accuracy_score(self.testY, preds_linear)
        print(f'Accuracy: {accuracy}')
        return accuracy
