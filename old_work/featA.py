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

        self.data={
            'Awickets_per_inning':[],
            'Afive_wicket_hauls_frac':[],
            'Adots_frac':[],
            'Aavg_economy':[],
            'Aavg_strike_rate':[],
            'Aavg_boundaries':[],
            'Aavg_runs':[],
            'Afifties_frac':[],
            'Bwickets_per_inning':[],
            'Bfive_wicket_hauls_frac':[],
            'Bdots_frac':[],
            'Bavg_economy':[],
            'Bavg_strike_rate':[],
            'Bavg_boundaries':[],
            'Bavg_runs':[],
            'Bfifties_frac':[]
        }

        self.player_level_cols=self.data.keys()

        self.five_wicket_bowlers=[]
        self.avg_economy=[]
        self.dots_frac=[]
        self.wickets_per_inning=[]

        self.avg_runs=[]
        self.avg_strike_rate=[]
        self.fifty_batsmen=[]
        self.avg_boundaries=[]

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

        # print(len(self.bowl))
        # print(len(self.bat))

        self.momentum_score_arr.append(self.momentum_score(row))
        self.location_score_arr.append(self.location_score(row))
        if self.batting_score(teamB)==0:
            self.batting_score_arr.append(1)
        else:
            if(self.batting_score(teamA)>self.batting_score(teamB)):
                self.batting_score_arr.append(1)
                # self.batting_score_arr.append(self.batting_score(teamA)/self.batting_score(teamB))
            else:
                self.batting_score_arr.append(0)
        if self.bowling_score(teamB)==0:
            self.bowling_score_arr.append(1)
        else:
            if(self.bowling_score(teamA)>self.bowling_score(teamB)):
                self.bowling_score_arr.append(1)
                # self.batting_score_arr.append(self.batting_score(teamA)/self.batting_score(teamB))
            else:
                self.bowling_score_arr.append(0)
            #self.bowling_score_arr.append(self.bowling_score(teamA)/self.bowling_score(teamB))
        
        teamA_players=row['team1_roster_ids'].split(':')
        teamB_players=row['team2_roster_ids'].split(':')

        Abowl1=[]
        Bbowl1=[]

        Abowl2=[]
        Bbowl2=[]

        Abowl3=[]
        Bbowl3=[]

        Abowl4=[]
        Bbowl4=[]

        Abat1=[]
        Bbat1=[]

        Abat2=[]
        Bbat2=[]

        Abat3=[]
        Bbat3=[]

        Abat4=[]
        Bbat4=[]

        for player in teamA_players:

            bowl1,bowl2,bowl3,bowl4=self.get_player_bowling_score(player)
            bat1,bat2,bat3,bat4=self.get_player_batting_score(player)

            Abowl1.append(bowl1)
            Abowl2.append(bowl2)
            Abowl3.append(bowl3)
            Abowl4.append(bowl4)

            Abat1.append(bat1)
            Abat2.append(bat2)
            Abat3.append(bat3)
            Abat4.append(bat4)
        
        for player in teamB_players:

            bowl1,bowl2,bowl3,bowl4=self.get_player_bowling_score(player)
            bat1,bat2,bat3,bat4=self.get_player_batting_score(player)

            Bbowl1.append(bowl1)
            Bbowl2.append(bowl2)
            Bbowl3.append(bowl3)
            Bbowl4.append(bowl4)

            Bbat1.append(bat1)
            Bbat2.append(bat2)
            Bbat3.append(bat3)
            Bbat4.append(bat4)
        
        Abowl4.sort()
        Bbowl4.sort()

        Abowl1.sort(reverse=True)
        Abowl2.sort(reverse=True)
        Abowl3.sort(reverse=True)

        Bbowl1.sort(reverse=True)
        Bbowl2.sort(reverse=True)
        Bbowl3.sort(reverse=True)

        Abat4.sort(reverse=True)
        Bbat4.sort(reverse=True)

        Abat1.sort(reverse=True)
        Abat2.sort(reverse=True)
        Abat3.sort(reverse=True)

        Bbat1.sort(reverse=True)
        Bbat2.sort(reverse=True)
        Bbat3.sort(reverse=True)

        curr_player_level_data={
            'Awickets_per_inning':sum(Abowl1[:3])/3,
            'Afive_wicket_hauls_frac':sum(Abowl2[:3])/3,
            'Adots_frac':sum(Abowl3[:4])/4,
            'Aavg_economy':sum(Abowl4[:4])/4,
            'Aavg_strike_rate':sum(Abat1[:5])/5,
            'Aavg_boundaries':sum(Abat2[:4])/4,
            'Aavg_runs':sum(Abat3[:5])/5,
            'Afifties_frac':sum(Abat4[:4])/4,
            'Bwickets_per_inning':sum(Bbowl1[:3])/3,
            'Bfive_wicket_hauls_frac':sum(Bbowl2[:3])/3,
            'Bdots_frac':sum(Bbowl3[:4])/4,
            'Bavg_economy':sum(Bbowl4[:4])/4,
            'Bavg_strike_rate':sum(Bbat1[:5])/5,
            'Bavg_boundaries':sum(Bbat2[:4])/4,
            'Bavg_runs':sum(Bbat3[:5])/5,
            'Bfifties_frac':sum(Bbat4[:4])/4,
        }


        for col in self.player_level_cols:
            self.data[col].append(curr_player_level_data[col])            
    
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

        if(team1wins>team2wins):
            return 1
        
        
        return 0
    
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
        
        self.TRAIN['win_val']=(self.TRAIN['winner_id']==self.TRAIN['team1_id'])

        winnner_val=[]
        toss_decision=[]

        for i in range(len(self.TRAIN)):

            if(self.TRAIN['win_val'][i]):
                winnner_val.append(1)
            else:
                winnner_val.append(0)
            
            if(self.TRAIN['toss winner'][i]==self.TRAIN['team1'][i]):
                toss_decision.append(1)
            else:
                toss_decision.append(0)
        
        self.TRAIN['winner']=winnner_val
        self.TRAIN['toss_winner']=toss_decision

        relevant_cols=['match id','team1_id','team2_id','team_count_50runs_last15','team_winp_last5','team1only_avg_runs_last15','team1_winp_team2_last15','ground_avg_runs_last15','momentum_score','location_score','batting_score','bowling_score','toss_winner','winner']

        for col in self.player_level_cols:
            self.TRAIN[col]=self.data[col]
            relevant_cols.append(col)
        
        TRAIN_FINAL=self.TRAIN[relevant_cols]

        TRAIN_FINAL.to_csv('training_set_player_level.csv',index=False)
    
    def get_player_bowling_score(self,player_id):

        bowling_performance=self.bowl[self.bowl['bowler_id']==float(player_id)]

        if(len(bowling_performance)==0):
            return 0,0,0,0
        
        #print("here")

        wickets_per_inning=sum(bowling_performance['wicket_count'])/len(bowling_performance)
        five_wicket_hauls_frac=len(bowling_performance[bowling_performance['wicket_count']>=5])/len(bowling_performance)
        dots_frac=sum(bowling_performance['dots'])/sum(bowling_performance['balls_bowled'])
        avg_economy=sum(bowling_performance['economy'])/len(bowling_performance)

        print(f'{player_id}: {wickets_per_inning},{five_wicket_hauls_frac},{dots_frac},{avg_economy}')

        return wickets_per_inning,five_wicket_hauls_frac,dots_frac,avg_economy
    
    def get_player_batting_score(self,player_id):

        batting_performance=self.bat[self.bat['batsman_id']==float(player_id)]

        if(len(batting_performance)==0):
            return 0,0,0,0
        
        avg_strike_rate=sum(batting_performance['strike_rate'])/len(batting_performance)
        avg_boundaries=(sum(batting_performance['Fours'])+sum(batting_performance['Sixes']))/len(batting_performance)
        avg_runs=sum(batting_performance['runs'])/len(batting_performance)

        fifties_frac=len(batting_performance['runs']>=50)/len(batting_performance)

        return avg_strike_rate,avg_boundaries,avg_runs,fifties_frac
    


