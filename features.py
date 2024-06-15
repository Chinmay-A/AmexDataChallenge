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

        self.data={
            'bat_above_50_a':[],
            'bat_above_50_b':[],
            'bat_above_75_a':[],
            'bat_above_75_b':[],
            'wickets_in_inning_a':[],
            'wickets_in_inning_b':[],
            'runs_in_inning_a':[],
            'runs_in_inning_b':[],
            'direct_encounter':[],
            'winner':[],
        }

        self.cols=self.data.keys()


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

    def batsman_above_fifty(self,row):

        playersA=row['team1_roster_ids'].split(':')
        playersB=row['team2_roster_ids'].split(':')

        teamA=0
        teamB=0

        for player in playersA:

            player_games=self.bat[self.bat['batsman_id']==float(player)]
            if(len(player_games)==0):
                continue
            games_above_fifty=len(player_games[player_games['runs']>=50])/len(player_games)
            teamA+=games_above_fifty
        
        for player in playersB:

            player_games=self.bat[self.bat['batsman_id']==float(player)]
            if(len(player_games)==0):
                continue
            games_above_fifty=len(player_games[player_games['runs']>=50])/len(player_games)
            teamB+=games_above_fifty
        
        return teamA,teamB
    
    def batsman_above_seventy_five(self,row):

        playersA=row['team1_roster_ids'].split(':')
        playersB=row['team2_roster_ids'].split(':')

        teamA=0
        teamB=0

        for player in playersA:

            player_games=self.bat[self.bat['batsman_id']==float(player)]
            if(len(player_games)==0):
                continue
            games_above_fifty=len(player_games[player_games['runs']>=75])/len(player_games)
            teamA+=games_above_fifty
        
        for player in playersB:

            player_games=self.bat[self.bat['batsman_id']==float(player)]
            if(len(player_games)==0):
                continue
            games_above_fifty=len(player_games[player_games['runs']>=75])/len(player_games)
            teamB+=games_above_fifty
        
        return teamA,teamB
    
    def wickets_in_inning(self,row):

        teamAbowl=self.matchlevel[self.matchlevel['team1_id']==row['team1_id']]
        teamBbowl=self.matchlevel[self.matchlevel['team2_id']==row['team2_id']]
        if(len(teamAbowl)==0 and len(teamBbowl)==0):
            return 0.4,0.4
        elif(len(teamAbowl)==0):
            avg_wicket_performBtemp=sum(teamBbowl['inning1_wickets'])/len(teamBbowl)
            return 0.4, avg_wicket_performBtemp
        elif(len(teamBbowl)==0):
            avg_wicket_performAtemp=sum(teamAbowl['inning2_wickets'])/len(teamAbowl)
            return avg_wicket_performAtemp,0.4

        avg_wicket_performA=sum(teamAbowl['inning2_wickets'])/len(teamAbowl)
        
        avg_wicket_performB=sum(teamBbowl['inning1_wickets'])/len(teamBbowl)

        return avg_wicket_performA,avg_wicket_performB
    
    def avg_runs_perform(self,row):

        teamAbat=self.matchlevel[self.matchlevel['team1_id']==row['team1_id']]
        teamBbat=self.matchlevel[self.matchlevel['team2_id']==row['team2_id']]

        if(len(teamAbat)==0 and len(teamBbat)==0):
            return 140,140
        elif(len(teamAbat)==0):
            avg_run_performBtemp=sum(teamBbat['inning2_runs'])/len(teamBbat)
            return 140, avg_run_performBtemp
        elif(len(teamBbat)==0):
            avg_run_performAtemp=sum(teamAbat['inning1_runs'])/len(teamAbat)
            return avg_run_performAtemp,140
        
        avg_run_performA=sum(teamAbat['inning1_runs'])/len(teamAbat)
        avg_run_performB=sum(teamBbat['inning2_runs'])/len(teamBbat)

        return avg_run_performA,avg_run_performB
    
    def direct_encounter(self,row):

        teamA1=self.matchlevel[(self.matchlevel['team1_id']==row['team1_id']) & (self.matchlevel['team2_id']==row['team2_id'])]
        teamA2=self.matchlevel[(self.matchlevel['team1_id']==row['team2_id']) & (self.matchlevel['team2_id']==row['team1_id'])]

        if(len(teamA1)==0 and len(teamA2)==0):
            return 0.5
        
        direct_encounter_score=(len(teamA1[teamA1['winner_id']==row['team1_id']])+len(teamA2[teamA2['winner_id']==row['team1_id']]))/(len(teamA1)+len(teamA2))

        return direct_encounter_score
    
    def process_row(self,row):

        # teamA=row['team1_id']
        # teamB=row['team2_id']

        match_date=row['match_dt']

        self.initialize(match_date)

        a,b=self.batsman_above_fifty(row)
        c,d=self.batsman_above_seventy_five(row)
        e,f=self.wickets_in_inning(row)
        g,h=self.avg_runs_perform(row)
        di=self.direct_encounter(row)

        winner=1

        if row['winner_id']==row['team2_id']:
            winner=0

        curr_data={
            'bat_above_50_a':a,
            'bat_above_50_b':b,
            'bat_above_75_a':c,
            'bat_above_75_b':d,
            'wickets_in_inning_a':e,
            'wickets_in_inning_b':f,
            'runs_in_inning_a':g,
            'runs_in_inning_b':h,
            'direct_encounter':di,
            'winner':winner,
        }

        for col in self.cols:
            self.data[col].append(curr_data[col])
        

    def generate_training_data(self):

        n=len(self.TRAIN)

        for i in range(n):
            curr_row=self.TRAIN.iloc[i]
            match_id=curr_row['match id']
            print(f'processing match: { match_id }')
            self.process_row(curr_row) 
        
        new_df=pd.DataFrame(self.data)

        new_df.to_csv('new_dataset.csv',index=False)
