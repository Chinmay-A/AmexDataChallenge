from .basic_features import f1

# to add a new feature, do the following steps:
# 1. Add the feature name with description in the `features` dictionary below
# 2. Write the feature generator in any file in utils and import it in the this file
# 3. Add the feature generator function in the `feature` dictionary below
# 4. to use the feature, just add the feature name in the `use_features` list in the `preprocessing.py` file

# for each feature, the generator should follow this template
# It should take input the row of the dataframe and data filtered to be used by it
# it should return a single value, the value of the feature

features = {
    'feature1': {
        'description': 'This is feature1',
        'generator': f1
    },
    'x1': {
        'description': 'This is x0',
    },
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
            'colsample_bytree':0.8
        },
        'num_rounds': 500,
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
        'num_rounds': 500,
    },
    'catboost': {
        'params': {
            'iterations': 500,
            'learning_rate': 0.1,
            'depth': 6
        },
    },
}