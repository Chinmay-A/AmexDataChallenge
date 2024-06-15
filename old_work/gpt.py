import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, RepeatedStratifiedKFold
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from catboost import CatBoostClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

class Model:
    
    def __init__(self, train_data: pd.DataFrame) -> None:
        self.train_data = train_data
        self.train, self.validate = train_test_split(self.train_data, train_size=0.75, random_state=42)
        
        self.trainY = self.train['winner']
        self.trainX = self.train.drop('winner', axis=1)
        self.trainX = self.trainX.fillna(0)
        
        self.testY = self.validate['winner']
        self.testX = self.validate.drop('winner', axis=1)
        self.testX = self.testX.fillna(0)

        self.scaler = StandardScaler()
        self.trainX = self.scaler.fit_transform(self.trainX)
        self.testX = self.scaler.transform(self.testX)
        
        print("Initialization successful")
    
    def train_model(self):
        smote = SMOTE(random_state=42)
        gb_params = {
            'n_estimators': [80, 100, 150],
            'max_depth': [3, 4, 5],
            'learning_rate': [0.01, 0.1, 0.2]
        }
        self.modelGBMA = GradientBoostingClassifier()
        self.modelGBMA = GridSearchCV(self.modelGBMA, gb_params, cv=5, scoring='accuracy')
        
        cat_params = {
            'iterations': [50, 100, 150],
            'depth': [3, 4, 5],
            'learning_rate': [0.01, 0.1, 0.2]
        }
        self.catmodel = CatBoostClassifier(verbose=0)
        self.catmodel = GridSearchCV(self.catmodel, cat_params, cv=5, scoring='accuracy')

        imb_pipeline_gbm = ImbPipeline(steps=[('smote', smote), ('model', self.modelGBMA)])
        imb_pipeline_cat = ImbPipeline(steps=[('smote', smote), ('model', self.catmodel)])
        
        imb_pipeline_gbm.fit(self.trainX, self.trainY)
        imb_pipeline_cat.fit(self.trainX, self.trainY)

        self.modelGBMA = imb_pipeline_gbm.named_steps['model'].best_estimator_
        self.catmodel = imb_pipeline_cat.named_steps['model'].best_estimator_

        self.evaluate()
        
    def predict(self):
        predsA = self.modelGBMA.predict_proba(self.testX)[:, 1]
        predsC = self.catmodel.predict_proba(self.testX)[:, 1]

        net_pred = (predsA + predsC) / 2
        return net_pred
    
    def evaluate(self):
        preds = self.predict()
        preds_linear = [1 if pred > 0.5 else 0 for pred in preds]
        accuracy = accuracy_score(self.testY, preds_linear)
        print(f'Accuracy: {accuracy}')
        return accuracy

# Example usage:
# Assuming `df` is your DataFrame containing the data with a 'winner' column.
# model = Model(df)
# model.train_model()
