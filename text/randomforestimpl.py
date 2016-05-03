# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from numpy import genfromtxt, savetxt
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt

targetFeatures = {"gender" : 84, "age" : 83, "ope" : 85, "con" : 86, "ext" : 87, "agr" : 88, "neu" : 89}
featureNames = ["gender", "age", "ope", "con", "ext", "agr", "neu"]

def get_test_data(opts, field):
    test_records = {}
    liwc_file = "%s/LIWC.csv" % opts.inputdir

    with open(liwc_file,'rb') as file:
        for record in genfromtxt(file, delimiter=',', dtype=str, skip_header = 1):
            user_id = record[0]
            record = [float(_record) if i not in [0,83] else _record for i, _record in enumerate(record)]
            test_records[user_id] = record[1:82]
    return test_records

def bayes_randomforest_input(opts, profile_data, field):
    training_data = profile_data['training_data']
    testing_data  = profile_data['testing_data']

    target  = []
    add_train_target = target.append
    liwcFeatures = []
    add_train_feature = liwcFeatures.append

    trueVal = []
    add_test_target = trueVal.append
    testFeatures = []
    add_test_feature = testFeatures.append

    test_records = {}

    liwc_file = "%s/LIWC.csv" % opts.inputdir

    from .megam_input import class_fncs
    class_fnc = class_fncs[field]
    with open(liwc_file,'rb') as file:
        for record in genfromtxt(file, delimiter=',', dtype=str, skip_header = 1):
            record = [float(_record) if i not in [0,83] else _record for i, _record in enumerate(record)]
            user_id = record[0]
            
            if user_id in training_data:
                feature_val = class_fnc(training_data[user_id][field])
                add_train_target(feature_val)
                add_train_feature(record[1:82])
            else:
                feature_val = class_fnc(testing_data[user_id][field])
                test_records[user_id] = record[1:82]
                add_test_target(feature_val)
                add_test_feature(record[1:82])

    if field in ['age', 'gender']:
        randForest = RandomForestClassifier(n_estimators=500, n_jobs = 2)
        randForest.fit(liwcFeatures, target)
    else:
        randForest = RandomForestRegressor(n_estimators=500, n_jobs = 2)
        randForest.fit(liwcFeatures, target)
    return randForest
