import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import numpy as np
import pandas as pd
import utils

def load_xgb_model():
    model = xgb.Booster()
    model.load_model('./out/xgb_model.json')
    return model

def load_lgbm_model():
    model = lgb.Booster(model_file='./out/lgbm_model.json')
    return model

def load_catboost_model():
    model = CatBoostClassifier()
    model.load_model('./out/catboost_model.json')
    return model

xgb_model = load_xgb_model()
lgbm_model = load_lgbm_model()
catboost_model = load_catboost_model()

def get_predictions(data):
    xgb_preds = xgb_model.predict(xgb.DMatrix(data, feature_names=list(trainX.columns)))
    lgbm_preds = lgbm_model.predict(data)
    catboost_preds = catboost_model.predict(data)
    return xgb_preds, lgbm_preds, catboost_preds

def ensemble_predictions(data):
    xgb_preds, lgbm_preds, catboost_preds = get_predictions(data)
    ensemble_preds = (utils.ensemble_ratio['xgboost'] * xgb_preds) + \
        (utils.ensemble_ratio['lightgbm'] * lgbm_preds) + \
        (utils.ensemble_ratio['catboost'] * catboost_preds)
    return ensemble_preds

def predict(data):
    data_np = np.array(data)
    ensemble_preds = ensemble_predictions(data_np)
    return ensemble_preds

def get_feature_scores():
    feature_scores = {
        'xgboost': xgb_model.get_score(importance_type='weight'),
        'lightgbm': lgbm_model.feature_importance(importance_type='split'),
        'catboost': catboost_model.get_feature_importance()
    }

    for col in utils.features.keys():
        utils.features[col]['score'] = 0.0

    for col in feature_scores['xgboost'].keys():
        utils.features[col]['score'] += feature_scores['xgboost'][col]
    for i, col in enumerate(trainX.columns):
        utils.features[col]['score'] += feature_scores['lightgbm'][i]
    for i, col in enumerate(trainX.columns):
        utils.features[col]['score'] += feature_scores['catboost'][i]

    for col in utils.features.keys():
        utils.features[col]['score'] /= 3

    total_score = 0.0
    for col in utils.features.keys():
        total_score += utils.features[col]['score']
    for col in utils.features.keys():
        utils.features[col]['score'] /= total_score
        utils.features[col]['score'] *= 100

    sorted_features = sorted(utils.features.items(), key=lambda x: x[1]['score'], reverse=True)
    for i, feature in enumerate(sorted_features):
        feature[1]['id'] = i+1
    return sorted_features

# Load the data
trainX = pd.read_csv('./out/dataX.csv')
testX = pd.read_csv('./out/testX.csv')

rawTrain = pd.read_csv('./datasets/train_data.csv')
rawTest = pd.read_csv('./datasets/test_data.csv')

predTrain = predict(trainX)
predTest = predict(testX)

# get features importances
feature_with_importances = get_feature_scores()

def get_output_csv1():
    # train_output = pd.DataFrame({
    #     'match id': rawTrain['match id'],
    #     'dataset_type': 'train'
    # })
    # train_output['win_pred_team_id'] = np.where(predTrain > 0.5, rawTrain['team1_id'], rawTrain['team2_id'])
    # train_output['win_pred_score'] = predTrain
    # train_output['train_algorithm'] = 'xgboost;lightgbm;catboost'
    # train_output['is_ensemble'] = 'yes'
    # train_output['train_hps_trees'] = str(utils.hyperparams['xgboost']['num_rounds']) + ';' + \
    #     str(utils.hyperparams['lightgbm']['num_rounds']) + ';' + str(utils.hyperparams['catboost']['params']['iterations'])
    # train_output['train_hps_depth'] = str(utils.hyperparams['xgboost']['params']['max_depth']) + ';' + \
    #     str(utils.hyperparams['lightgbm']['params']['max_depth']) + ';' + str(utils.hyperparams['catboost']['params']['depth'])
    # train_output['train_hps_lr'] = str(utils.hyperparams['xgboost']['params']['eta']) + ';' + \
    #     str(utils.hyperparams['lightgbm']['params']['learning_rate']) + ';' + str(utils.hyperparams['catboost']['params']['learning_rate'])

    top10_features = feature_with_importances[:min(10, len(feature_with_importances))]
    # for i in range(10):
    #     if i < len(top10_features):
    #         train_output[f'indep_feat_id{i+1}'] = trainX[top10_features[i][0]]
    #     else:
    #         train_output[f'indep_feat_id{i+1}'] = 0

    test_output = pd.DataFrame({
        'match id': rawTest['match id'],
        'dataset_type': 'r2'
    })
    test_output['win_pred_team_id'] = np.where(predTest > 0.5, rawTest['team1_id'], rawTest['team2_id'])
    test_output['win_pred_score'] = predTest
    test_output['train_algorithm'] = 'xgboost;lightgbm;catboost'
    test_output['is_ensemble'] = 'yes'
    test_output['train_hps_trees'] = str(utils.hyperparams['xgboost']['num_rounds']) + ';' + \
        str(utils.hyperparams['lightgbm']['num_rounds']) + ';' + str(utils.hyperparams['catboost']['params']['iterations'])
    test_output['train_hps_depth'] = str(utils.hyperparams['xgboost']['params']['max_depth']) + ';' + \
        str(utils.hyperparams['lightgbm']['params']['max_depth']) + ';' + str(utils.hyperparams['catboost']['params']['depth'])
    test_output['train_hps_lr'] = str(utils.hyperparams['xgboost']['params']['eta']) + ';' + \
        str(utils.hyperparams['lightgbm']['params']['learning_rate']) + ';' + str(utils.hyperparams['catboost']['params']['learning_rate'])

        
    for i in range(10):
        if i < len(top10_features):
            test_output[f'indep_feat_id{i+1}'] = testX[top10_features[i][0]]
        else:
            test_output[f'indep_feat_id{i+1}'] = 0
    
    # output_csv1 = pd.concat([train_output, test_output])
    # output_csv1.to_csv('./out/2024_DS_Track_File1_chinmayaons1.csv', index=False)
    test_output.to_csv('./out/2024_DS_Track_File1_chinmayaons1.csv', index=False)
    print("Output CSV1 generated successfully")

get_output_csv1()

def get_output_csv2():
    top100_features = feature_with_importances[:min(100, len(feature_with_importances))]
    output_csv2 = pd.DataFrame(columns=['feat_id', 'feat_name', 'feat_description', 'model_feat_imp_train', 'feat_rank_train'])
    for feature in top100_features:
        if feature[1]['score'] <= 0.0001:
            break
        output_csv2 = output_csv2._append({
            'feat_id': feature[1]['id'],
            'feat_name': feature[0],
            'feat_description': feature[1]['description'],
            'model_feat_imp_train': np.round(feature[1]['score'], 2),
            'feat_rank_train': feature[1]['id']
        }, ignore_index=True)

    output_csv2.to_csv('./out/2024_DS_Track_File2_chinmayaons1.csv', index=False)
    print("Output CSV2 generated successfully")

# get_output_csv2()