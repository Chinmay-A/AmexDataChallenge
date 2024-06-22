import utils
import pandas as pd
import numpy as np

# use_features = ['feature1']
use_features = utils.features.keys()

raw_data = {
    'bat': pd.read_csv('./datasets/batsman_data.csv'),
    'bowl': pd.read_csv('./datasets/bowler_data.csv'),
    'match': pd.read_csv('./datasets/match_level_data.csv'),
    'train': pd.read_csv('./datasets/train_data.csv'),
    'test': pd.read_csv('./datasets/test_data.csv'),
}

for key in raw_data:
    raw_data[key]['match_dt'] = pd.to_datetime(raw_data[key]['match_dt'], format='%Y-%m-%d')

def filter_data(data, match_date):
    filtered_data = {}
    for key in data:
        filtered_data[key] = data[key][data[key]['match_dt'] < match_date]

    return filtered_data

def preprocess(data):
    preprocessed_data = []
    for i, row in enumerate(data.iterrows()):
        if (i+1) % 100 == 0:
            print(f'Processing row {i+1}')
        
        filtered_data = filter_data(raw_data, row[1]['match_dt'])
        row_feat = []
        for feature in use_features:
            row_feat.append(utils.features[feature]['generator'](row[1], filtered_data))
        preprocessed_data.append(row_feat)
    
    df = pd.DataFrame(preprocessed_data, columns=use_features)
    return df

print('Preprocessing train data')
trainX = preprocess(raw_data['train'])
print('Preprocessing test data')
testX = preprocess(raw_data['test'])

print("Generating data files.")
trainX.to_csv('./out/dataX.csv', index=False)
testX.to_csv('./out/testX.csv', index=False)

trainY = np.array(raw_data['train']['winner_id'])
trainY = np.where(trainY == raw_data['train']['team1_id'], 1, 0)
trainY = pd.DataFrame(trainY, columns=['winner'])
trainY.to_csv('./out/dataY.csv', index=False)

print("Data files generated successfully.")