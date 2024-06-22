from .basic_features import *
from .slightly_complex import *

# to add a new feature, do the following steps:
# 1. Add the feature name with description in the `features` dictionary below
# 2. Write the feature generator in any file in utils and import it in the this file
# 3. Add the feature generator function in the `feature` dictionary below
# 4. to use the feature, just add the feature name in the `use_features` list in the `preprocessing.py` file

# for each feature, the generator should follow this template
# It should take input the row of the dataframe and data filtered to be used by it
# it should return a single value, the value of the feature

features = {
    # 'lighting': {
    #     'description': 'Label encoding of the lighting condition of the match',
    #     'generator': lighting
    # },
    'team1v2_win_prob': {
        'description': 'Win probability of team1 against team2',
        'generator': team1v2_win_prob
    },
    # 'team1_games_played': {
    #     'description': 'Number of games played by team1',
    #     'generator': team1_games_played
    # },
    # 'team2_games_played': {
    #     'description': 'Number of games played by team2',
    #     'generator': team2_games_played
    # },
    # 'more_games_played': {
    #     'description': 'Whether team1 has played more games than team2',
    #     'generator': played_more_games
    # },
    'much_more_games_played': {
        'description': 'Whether either of the team has played much more games than the other team',
        'generator': much_more_games_played
    },
    # 'more_win_percent': {
    #     'description': 'Whether team1 has higher win percentage than team2',
    #     'generator': more_win_percent
    # },
    'winp_last5_categorized': {
        'description': 'Win probability of team1 in last 5 matches',
        'generator': winp_last5_categorized
    },
    # 'team1_win_prob': {
    #     'description': 'Win probability of team1 in all matches',
    #     'generator': team1_win_prob
    # },
    # 'team2_win_prob': {
    #     'description': 'Win probability of team2 in all matches',
    #     'generator': team2_win_prob
    # },

}

ensemble_ratio = {
    'xgboost': 0.33,
    'lightgbm': 0.33,
    'catboost': 0.34,
}

hyperparams = {
    'xgboost': {
        'params': {
            'objective':'binary:logistic',
            'eval_metric':'logloss',
            'max_depth':6,
            'eta':0.1,
            'verbosity': 0,
            'subsample':0.8,
            'colsample_bytree':0.8,
        },
        'num_rounds': 100,
    },
    'lightgbm': {
        'params': {
            'objective':'binary',
            'metric':'binary_logloss',
            'max_depth':6,
            'learning_rate':0.1,
            'verbosity': -1,
            'subsample':0.8,
            'colsample_bytree':0.8
        },
        'num_rounds': 100,
    },
    'catboost': {
        'params': {
            'iterations': 100,
            'learning_rate': 0.1,
            'depth': 6
        },
    },
}