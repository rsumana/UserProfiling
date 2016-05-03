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

targetFeatures = {"gender" : 2, "age" : 1, "ope" : 3, "con" : 4, "ext" : 5, "agr" : 6, "neu" : 7}
featureNames = ["gender", "age", "ope", "con", "ext", "agr", "neu"]

def get_test_data_likes(opts, profile_data, field):
    training_data = profile_data['training_data']
    testing_data  = profile_data['testing_data']

    userid_relations = {}
    file = "%s/relation/relation.csv" % opts.inputdir
    for i,userid,likeid in genfromtxt(file, delimiter=',', dtype=str, skip_header = 1):
        if userid in testing_data:
            try:
                userid_relations[userid].append(likeid)
            except KeyError:
                userid_relations[userid] = [likeid]
    import pickle
    try:
        profile_map = pickle.load(open("text/models/profile_map.pickle", "rb"))
    except IOError:
        category_hash = {}
        profile_map   = {}
        with open("scrapper/pagelikes.csv",'rb') as file:
            for i,record in enumerate(genfromtxt(file, delimiter=',', dtype=str, skip_header = 1)):
                if i % 100 == 0:
                    print(i)
                like_id      = record[0]
                page_type    = record[1][1:-1]
                category_val = category_hash.get(page_type)
                if not category_val:
                    category_val = len(category_hash)
                    category_hash[page_type] = category_val
                values = [float(_val) for _val in record[2:]]
                profile_map[like_id] = [category_val] + values
        pickle.dump(profile_map, open("text/models/profile_map.pickle", "wb"))
    test_records = {}
    for user_id,relations in userid_relations.items():
        for relation in relations:
            relation_val = profile_map.get(relation)
            if relation_val:
                try:
                    test_records[user_id].append(relation_val)
                except KeyError:
                    test_records[user_id] = [relation_val]
    return test_records

def aget_test_data_likes(opts, profile_data, field):
    training_data = profile_data['training_data']
    testing_data  = profile_data['testing_data']

    userid_relations = {}

    file = "%s/relation/relation.csv" % opts.inputdir
    for i,userid,likeid in genfromtxt(file, delimiter=',', dtype=str, skip_header = 1):
        if userid in testing_data:
            try:
                userid_relations[userid].append(likeid)
            except KeyError:
                userid_relations[userid] = [likeid]
    print(len(training_data), len(testing_data))

    import pickle
    try:
        raise IOError
        profile_map = pickle.load(open("scrapper/profilePageMap.csv.pickle", "rb"))
    except IOError:
        profile_map = {}
        update = profile_map.update

        with open("scrapper/profilePageMap_pageid.csv",'rb') as file:
            for i,record in enumerate(genfromtxt(file, delimiter=',', dtype=str, skip_header = 1)):
                if i % 100 == 0:
                    print(i)
                user_id = record[0][1:-1]
                page_id = record[1]
                values  = [float(_val) for _val in record[10:13]]
                profile_map[page_id] = values
    test_records = {}
    for user_id,relations in userid_relations.items():
        for relation in relations:
            relation_val = profile_map.get(relation)
            if relation_val:
                try:
                    test_records[user_id].append(relation_val)
                except KeyError:
                    test_records[user_id] = [relation_val]
    print(list(test_records.items())[0])
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

    #test_records = get_test_data_likes(opts, profile_data, field)

    """
    profile_map = get_test_data_likes(opts, profile_data, field)
    import pickle
    try:
        profile_map = pickle.load(open("scrapper/profilePageMap.csv.pickle", "rb"))
    except IOError:
        profile_map = {}
        update = profile_map.update

        with open("scrapper/profilePageMap.csv",'rb') as file:
            for i,record in enumerate(genfromtxt(file, delimiter=',', dtype=str, skip_header = 1)):
                print(i)
                user_id = record[0][1:-1]                                   
                values  = [float(_val) for _val in record[10:13]]
                try:
                    profile_map[user_id].append(values)
                except KeyError:
                    profile_map[user_id] = [values]
        pickle.dump(profile_map, open("scrapper/profilePageMap.csv.pickle", "wb"), protocol=2)
    """

    from .megam_input import class_fncs
    value_fnc = class_fncs.get(field)

    for user_id,user_data in training_data.items():
        target_val = value_fnc(training_data[user_id][field])
        for values in user_data['page_counts']:
            add_train_target(value_fnc(target_val))
            add_train_feature(values)

    for user_id,user_data in testing_data.items():
        target_val = value_fnc(testing_data[user_id][field])
        for values in user_data['page_counts']:
            add_test_target(value_fnc(target_val))
            add_test_feature(values)
    if field in ['age', 'gender']:
        randForest = RandomForestClassifier(n_estimators=500, n_jobs = 2)
        randForest.fit(liwcFeatures, target)
        return randForest
    else:
        randForest = RandomForestRegressor(n_estimators=500, n_jobs = 2)
        randForest.fit(liwcFeatures, target)
        return randForest


    for user_id,bucket in profile_map.items():
        if user_id in training_data:
            target_val = training_data[user_id][field]
            for values in bucket:
                add_train_target(value_fnc(target_val))
                add_train_feature(values)
        else:
            target_val = testing_data[user_id][field]
            for values in bucket:
                try:
                    test_records[user_id] = [values]
                except KeyError:
                    test_records[user_id].append(values)
                #add_test_target(value_fnc(target_val))
                #add_test_feature(values)
    print(len(target), len(trueVal))

    if field in ['age', 'gender']:
        randForest = RandomForestClassifier(n_estimators=500, n_jobs = 2)
        randForest.fit(liwcFeatures, target)
        return randForest, test_records

        predFeature = randForest.predict(testFeatures)
        featureAccuracy = accuracy_score(trueVal, predFeature)

        print(field + " accuracy : " + str(featureAccuracy))

        gnb = GaussianNB()
        predFeature = gnb.fit(liwcFeatures, target).predict(testFeatures)

        #Prediction using Testing Data and find accuracy
        featureAccuracy = accuracy_score(trueVal, predFeature)
        print(field + " accuracy : " + str(featureAccuracy))
    else:
        #Training
        randForest = RandomForestRegressor(n_estimators=500, n_jobs = 2)
        randForest.fit(liwcFeatures, target)
        return randForest, test_records

        #Prediction using Testing Data and find accuracy
        lr = LinearRegression()
        lr.fit(liwcFeatures, target)
        return lr, test_records
        predFeature = lr.fit(liwcFeatures, target).predict(testFeatures)

        rmse = sqrt(mean_squared_error(trueVal, predFeature))
        mae = mean_absolute_error(trueVal, predFeature)
        print(field + " MAE : " + str(mae))
        print(field + " RMSE : " + str(rmse))

        #Prediction using Testing Data and find accuracy
        #predFeature = randForest.predict(testFeature)
        lr = LinearRegression()
        predFeature = lr.fit(liwcFeatures, target).predict(testFeatures)

        rmse = sqrt(mean_squared_error(trueVal, predFeature))
        mae = mean_absolute_error(trueVal, predFeature)
        print(field + " MAE : " + str(mae))
        print(field + " RMSE : " + str(rmse))

    return randForest,test_records,accuracy_score
