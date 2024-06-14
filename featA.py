import pandas as pd
import numpy as np
import statistics as stats

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

        self.momentum_score_arr=[]
        self.location_score_arr=[]
        self.batting_score_arr=[]
        self.bowling_score_arr=[]

        self.bowl=self.BOWLERS
        self.bat=self.BATSMEN
        self.train=self.TRAIN
        self.test=self.TEST
        self.matchlevel=self.MATCHLEVEL

    def initialize(self,date):
        # date = date[0]
        
        self.bowl=self.BOWLERS[self.BOWLERS['match_dt']<date]
        self.bat=self.BATSMEN[self.BATSMEN['match_dt']<date]
        self.train=self.TRAIN[self.TRAIN['match_dt']<date]
        self.test=self.TEST[self.TEST['match_dt']<date]
        self.matchlevel=self.MATCHLEVEL[self.MATCHLEVEL['match_dt']<date]

        self.bowl=self.bowl.sort_values(by=['match_dt'],ascending=False)
        self.bat=self.bat.sort_values(by=['match_dt'],ascending=False)
        self.train=self.train.sort_values(by=['match_dt'],ascending=False)
        self.test=self.test.sort_values(by=['match_dt'],ascending=False)
        self.matchlevel=self.matchlevel.sort_values(by=['match_dt'],ascending=False)
    
    def process_row(self,row):

        teamA=row['team1_id']
        teamB=row['team2_id']

        match_date=row['match_dt']

        # playersA=row['team1_roster_ids'].split(':')
        # playersB=row['team2_roster_ids'].split(':')
        # playersA=[int(i) for i in playersA]
        # playersB=[int(i) for i in playersB]
        
        self.initialize(match_date)

        self.momentum_score_arr.append(self.momentum_score(row))
        self.location_score_arr.append(self.location_score(row))
        if self.batting_score(teamB)==0:
            self.batting_score_arr.append(1)
        else:
            self.batting_score_arr.append(self.batting_score(teamA)/self.batting_score(teamB))
        if self.bowling_score(teamB)==0:
            self.bowling_score_arr.append(1)
        else:
            self.bowling_score_arr.append(self.bowling_score(teamA)/self.bowling_score(teamB))
    
    def location_score(self,row):

        toss_winner=row['toss winner']
        toss_decision=row['toss decision']

        relevant_games=self.matchlevel[self.matchlevel['ground_id']==row['ground_id']]

        if(len(relevant_games)>10):
            relevant_games=relevant_games.head(10)
        
        bowlfirstwins=len(relevant_games[relevant_games['by']=='runs'])
        batfirstwins=len(relevant_games[relevant_games['by']=='wickets'])

        if(bowlfirstwins>batfirstwins):
            if(toss_winner==row['team1'] and toss_decision=='field'):
                return 1
            elif(toss_winner==row['team2'] and toss_decision=='bat'):
                return 1
        else:
            if(toss_winner==row['team1'] and toss_decision=='bat'):
                return 1
            elif(toss_winner==row['team2'] and toss_decision=='field'):
                return 1
        
        return 0
    
    def momentum_score(self,row):

        relevantgamesA=self.matchlevel[(self.matchlevel['team1_id']==row['team1_id']) | (self.matchlevel['team2_id']==row['team1_id'])]
        relevantgamesB=self.matchlevel[(self.matchlevel['team1_id']==row['team2_id']) | (self.matchlevel['team2_id']==row['team2_id'])]
        
        if(len(relevantgamesA)>10):
            relevantgamesA=relevantgamesA.head(10)
        if(len(relevantgamesB)>10):
            relevantgamesB=relevantgamesB.head(10)
        
        team1wins=len(relevantgamesA[relevantgamesA['winner_id']==row['team1_id']])
        team2wins=len(relevantgamesB[relevantgamesB['winner_id']==row['team2_id']])

        if(team2wins==0):
            return 1
        
        return team1wins/team2wins
    
    def batting_score(self,teamid):

        relevantgamesA=self.matchlevel[(self.matchlevel['team1_id']==teamid) | (self.matchlevel['team2_id']==teamid)]

        if(len(relevantgamesA)>10):
            relevantgamesA=relevantgamesA.head(10)
        
        relevantgamesA.reset_index(inplace=True)
        
        runsbyA=[]
        for i in range(len(relevantgamesA)):

            if(relevantgamesA['team1_id'][i]==teamid and relevantgamesA['team1'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='bat'):
                runsbyA.append(relevantgamesA['inning1_runs'][i])
            elif(relevantgamesA['team1_id'][i]==teamid and relevantgamesA['team2'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='field'):
                runsbyA.append(relevantgamesA['inning1_runs'][i])
            elif(relevantgamesA['team1_id'][i]==teamid):
                runsbyA.append(relevantgamesA['inning2_runs'][i])
            elif(relevantgamesA['team2_id'][i]==teamid and relevantgamesA['team2'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='bat'):
                runsbyA.append(relevantgamesA['inning1_runs'][i])
            elif(relevantgamesA['team2_id'][i]==teamid and relevantgamesA['team1'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='field'):
                runsbyA.append(relevantgamesA['inning1_runs'][i])
            else:
                runsbyA.append(relevantgamesA['inning2_runs'][i])

        runsbyA = [float(i) for i in runsbyA]
        if len(runsbyA) <= 1 : return 0

        stddev=stats.stdev(runsbyA)
        mean=stats.mean(runsbyA)

        if stddev == 0: return 0
        
        if(len(runsbyA)<3):

            return (runsbyA[0]-mean)/stddev
        
        zscoresum=0

        for i in range(3):
            zscoresum+=(runsbyA[i]-mean)/stddev
        
        return zscoresum/3
    
    def bowling_score(self,teamid):

        relevantgamesA=self.matchlevel[(self.matchlevel['team1_id']==teamid) | (self.matchlevel['team2_id']==teamid)]

        if(len(relevantgamesA)>10):
            relevantgamesA=relevantgamesA.head(10)
        
        relevantgamesA.reset_index(inplace=True)
        
        wicketsbyA=[]

        for i in range(len(relevantgamesA)):

            if(relevantgamesA['team1_id'][i]==teamid and relevantgamesA['team1'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='field'):
                wicketsbyA.append(relevantgamesA['inning1_wickets'][i])
            elif(relevantgamesA['team1_id'][i]==teamid and relevantgamesA['team2'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='bat'):
                wicketsbyA.append(relevantgamesA['inning1_wickets'][i])
            elif(relevantgamesA['team1_id'][i]==teamid):
                wicketsbyA.append(relevantgamesA['inning2_wickets'][i])
            elif(relevantgamesA['team2_id'][i]==teamid and relevantgamesA['team2'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='field'):
                wicketsbyA.append(relevantgamesA['inning1_wickets'][i])
            elif(relevantgamesA['team2_id'][i]==teamid and relevantgamesA['team1'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='bat'):
                wicketsbyA.append(relevantgamesA['inning1_wickets'][i])
            else:
                wicketsbyA.append(relevantgamesA['inning2_wickets'][i])
        
        wicketsbyA = [float(i) for i in wicketsbyA]

        if len(wicketsbyA) <= 1: return 0

        stddev=stats.stdev(wicketsbyA)
        mean=stats.mean(wicketsbyA)
        if stddev == 0: return 0

        if(len(wicketsbyA)<3):

            return (wicketsbyA[0]-mean)/stddev
        
        zscoresum=0

        for i in range(3):
            zscoresum+=(wicketsbyA[i]-mean)/stddev
        
        return zscoresum/3

    def generate_training_data(self):

        n=len(self.TRAIN)

        #self.TRAIN.reset_index(inplace=True)

        for i in range(n):
            # print(i)
            curr_row=self.TRAIN.iloc[i]
            #print(curr_row)
            self.process_row(curr_row) 

        self.TRAIN['momentum_score']=self.momentum_score_arr
        self.TRAIN['location_score']=self.location_score_arr
        self.TRAIN['batting_score']=self.batting_score_arr
        self.TRAIN['bowling_score']=self.bowling_score_arr

        self.TRAIN.to_csv('training_set.csv',index=False)