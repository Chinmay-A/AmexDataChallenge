import pandas as pd
import numpy as np

class Data:

    def __init__(self):

        self.BOWLERS=pd.read_csv('bowler_data.csv')
        self.BATSMEN=pd.read_csv('batsman_data.csv')
        self.TRAIN=pd.read_csv('train_data.csv')
        self.TEST=pd.read_csv('test_data.csv')
        self.MATCHLEVEL=pd.read_csv('match_level_data.csv')

        self.BOWLERS['match_dt']=pd.to_datetime(self.BOWLERS['match_dt'], format='%Y-%m-%d')
        self.BATSMEN['match_dt']=pd.to_datetime(self.BATSMEN['match_dt'], format='%Y-%m-%d')
        self.TRAIN['match_dt']=pd.to_datetime(self.TRAIN['match_dt'], format='%Y-%m-%d')
        self.TEST['match_dt']=pd.to_datetime(self.TEST['match_dt'], format='%Y-%m-%d')
        self.MATCHLEVEL['match_dt']=pd.to_datetime(self.MATCHLEVEL['match_dt'], format='%Y-%m-%d')

        print(f"No of bowlers: {len(self.BOWLERS)}")

        self.bowl=self.BOWLERS
        self.bat=self.BATSMEN
        self.train=self.TRAIN
        self.test=self.TEST
        self.matchlevel=self.MATCHLEVEL

    def initialize(self,date):

        pd_date_time=pd.to_datetime(date,format='%Y-%m-%d')
        
        self.bowl=self.BOWLERS[self.BOWLERS['match_dt']<pd_date_time]
        self.bat=self.BATSMEN[self.BATSMEN['match_dt']<pd_date_time]
        self.train=self.TRAIN[self.TRAIN['match_dt']<pd_date_time]
        self.test=self.TEST[self.TEST['match_dt']<pd_date_time]
        self.matchlevel=self.MATCHLEVEL[self.MATCHLEVEL['match_dt']<pd_date_time]

        print(f"No of bowlers: {len(self.bowl)}")
    
    

    