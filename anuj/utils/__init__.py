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
    # 'team1v2_win_prob': {
    #     'description': 'Whether team1 has won more matches against team2 or not',
    #     'generator': team1v2_win_prob
    # },
    # 'much_more_games_played': {
    #     'description': 'Whether either of the team has played much more games than the other team',
    #     'generator': much_more_games_played
    # },
    'winp_last5_categorized': {
        'description': 'Win probability of team1 in last 5 matches',
        'generator': winp_last5_categorized
    },
    # 'inning1_perf': {
    #     'description': 'Performance of team1 in inning1 categorized with respect to average performance',
    #     'generator': inning1_perf
    # },
    # 'inning2_perf': {
    #     'description': 'Performance of team2 in inning2 categorized with respect to average performance',
    #     'generator': inning2_perf
    # },
    'has_good_bowlers': {
        'description': 'If team has some bowlers taking 4 wickets or more',
        'generator': has_good_bowlers
    },
    'has_good_batsman': {
        'description': 'If team has some batsmen getting 50 runs or more',
        'generator': has_good_batsmen
    },
    'usual_wins': {
        'description': 'Is the toss decision aligned with the teams strengths',
        'generator': usual_wins
    },
    'experience_score': {
        'description': 'Evaluates the experience of players who satisfy the performance criteria',
        'generator': experience_score
    },

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