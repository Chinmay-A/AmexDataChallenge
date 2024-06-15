import pandas as pd
from gpt import Model

train = pd.read_csv('./training_set_player_level.csv')
cols=['team_count_50runs_last15','team_winp_last5','team1only_avg_runs_last15','team1_winp_team2_last15','ground_avg_runs_last15']
#train=train[cols]
train.drop(columns=['match id','team1_id','team2_id'],inplace=True)
#train.drop(columns=cols,inplace=True)

modelA=Model(train)

modelA.train_model()
