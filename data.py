import pandas as pd
import numpy as np

class Data:

    def __init__(self):

        self.BOWLERS=pd.read_csv('bowler_data.csv')
        self.BATSMEN=pd.read_csv('batsman_data.csv')
        self.TRAIN=pd.read_csv('train_data.csv')
        self.TEST=pd.reaad_csv('test_data.csv')
        self.MATCHLEVEL=pd.read_csv('match_level_data.csv')

        self.bowl=self.BOWLERS
        self.bat=self.BATSMEN
        self.train=self.TRAIN
        self.test=self.TEST
        self.matchlevel=self.MATCHLEVEL

    def initialize(self,date):

        self.bowl=self.BOWLERS[self.BOWLERS['match_dt']<date]
        self.bat=self.BATSMEN[self.BATSMEN['match_dt']<date]
        self.train=self.TRAIN[self.TRAIN['match_dt']<date]
        self.test=self.TEST[self.TEST['match_dt']<date]
        self.matchlevel=self.MATCHLEVEL[self.MATCHLEVEL['match_dt']<date]
    

        