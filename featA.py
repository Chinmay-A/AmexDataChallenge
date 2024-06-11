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

        self.bowl=self.bowl.sort_values(by=['match_dt'],ascending=False)
        self.bat=self.bat.sort_values(by=['match_dt'],ascending=False)
        self.train=self.train.sort_values(by=['match_dt'],ascending=False)
        self.test=self.bowl.sort_values(by=['match_dt'],ascending=False)
        self.matchlevel=self.bowl.sort_values(by=['match_dt'],ascending=False)
    
    def process_row(self,row):

        teamA=row['team1_id']
        teamB=row['team2_id']

        match_date=row['match_dt']

        playersA=row['team1_roster_ids'].split(':')
        playersB=row['team2_roster_ids'].split(':')
        playersA=[int(i) for i in playersA]
        playersB=[int(i) for i in playersB]
        
        self.initialize(match_date)
    
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

        relevantgamesA=self.matchlevel[self.matchlevel['team1_id']==row['team1_id'] or self.matchlevel['team2_id']==row['team1_id']]
        relevantgamesB=self.matchlevel[self.matchlevel['team1_id']==row['team2_id'] or self.matchlevel['team2_id']==row['team2_id']]
        
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

        relevantgamesA=self.matchlevel[self.matchlevel['team1_id']==teamid or self.matchlevel['team2_id']==teamid]

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
                runsbyA.append(relevantgamesA['innigs1_runs'][i])
            elif(relevantgamesA['team2_id'][i]==teamid and relevantgamesA['team1'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='field'):
                runsbyA.append(relevantgamesA['innigs1_runs'][i])
            else:
                runsbyA.append(relevantgamesA['innings2_runs'][i])
        
        stddev=stats.stdev(runsbyA)
        mean=stats.mean(runsbyA)

        if(len(runsbyA)<3):

            return (runsbyA[0]-mean)/stddev
        
        zscoresum=0

        for i in range(3):
            zscoresum+=(runsbyA[i]-mean)/stddev
        
        return zscoresum/3
    
    def bowling_score(self,teamid):

        relevantgamesA=self.matchlevel[self.matchlevel['team1_id']==teamid or self.matchlevel['team2_id']==teamid]

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
                wicketsbyA.append(relevantgamesA['innigs1_wickets'][i])
            elif(relevantgamesA['team2_id'][i]==teamid and relevantgamesA['team1'][i]==relevantgamesA['toss winner'][i] and relevantgamesA['toss decision'][i]=='bat'):
                wicketsbyA.append(relevantgamesA['innigs1_wickets'][i])
            else:
                wicketsbyA.append(relevantgamesA['innings2_wickets'][i])
        
        stddev=stats.stdev(wicketsbyA)
        mean=stats.mean(wicketsbyA)

        if(len(wicketsbyA)<3):

            return (wicketsbyA[0]-mean)/stddev
        
        zscoresum=0

        for i in range(3):
            zscoresum+=(wicketsbyA[i]-mean)/stddev
        
        return zscoresum/3
        




        




