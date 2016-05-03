# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from numpy import genfromtxt, savetxt
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.tree import DecisionTreeRegressor,DecisionTreeClassifier
from math import sqrt

targetFeatures = {"gender" : 2, "age" : 1, "ope" : 3, "con" : 4, "ext" : 5, "agr" : 6, "neu" : 7}
featureNames = ["gender", "age", "ope", "con", "ext", "agr", "neu"]
#featureNames = ["ope", "con", "ext", "agr", "neu"]

categoryHash = {}


dataTrain = genfromtxt(open('scrapper/profilePageMap.csv','r'),delimiter=',',dtype = str, skip_header = 1)[:803082]    
dataTest = genfromtxt(open('scrapper/profilePageMap.csv','r'),delimiter=',',dtype = str)[803083:]

categoryIndex = 0
def replaceCategoryMap(pageFeatures):
    allPageFeatures = []
    global categoryIndex
    for x in pageFeatures:
        eachPage = []
        category = x[0]
        if(categoryHash.get(category) != None):
            eachPage.append(categoryHash.get(x[0]))
        else:
            categoryHash[category] = categoryIndex
            eachPage.append(categoryIndex)
            categoryIndex+=1
        eachPage.append(float(x[1]))
        eachPage.append(float(x[2]))
        eachPage.append(float(x[3]))
        allPageFeatures.append(eachPage)
    return allPageFeatures

def randomForestClass(feature):
    #Training Data
    featureValue = targetFeatures[feature]
    target = [float(x[featureValue]) for x in dataTrain]
    if(feature == "age"):
        target = getAgeRange(target)    
    pageFeatures = [x[9:13] for x in dataTrain]
    pageFeatures = replaceCategoryMap(pageFeatures)
    
    #Training
    randForest = RandomForestClassifier(n_estimators=24, n_jobs = 2)
    randForest.fit(pageFeatures, target)
    
    #Testing Data
    trueVal = [float(x[featureValue]) for x in dataTest]
    if(feature == "age"):
        trueVal = getAgeRange(trueVal)
    testFeatures = [x[9:13] for x in dataTest]
    testFeatures = replaceCategoryMap(testFeatures)
    
    #Prediction using Testing Data and find accuracy
    predFeature = randForest.predict(testFeatures)
    featureAccuracy = accuracy_score(trueVal, predFeature)
    
    print(feature + " accuracy : " + str(featureAccuracy))
    
def getAgeRange(data):
    ageCol = []
    for x in data:
        fltX = float(x)
        if fltX < 18:
            ageCol.append(0)
        elif fltX < 25:
            ageCol.append(1)
        elif fltX < 35:
            ageCol.append(2)
        elif fltX < 50:
            ageCol.append(3)
        else:
            ageCol.append(4)
    return ageCol

def randomForestRegr(feature):
    #Training Data
    featureValue = targetFeatures[feature]
    target = [float(x[featureValue]) for x in dataTrain]
    #target = target.reshape(-1, 1)
    pageFeatures = [x[9:13] for x in dataTrain]
    pageFeatures = replaceCategoryMap(pageFeatures)
    #Training
    randForest = RandomForestRegressor(n_estimators=24, n_jobs = 2)
    randForest.fit(pageFeatures, target)
    #Testing Data
    trueVal = [float(x[featureValue]) for x in dataTest]
    testFeature = [x[9:13] for x in dataTest]
    testFeature = replaceCategoryMap(testFeature)
    
    #Prediction using Testing Data and find accuracy
    predFeature = randForest.predict(testFeature)

    rmse = sqrt(mean_squared_error(trueVal, predFeature))
    mae = mean_absolute_error(trueVal, predFeature)
    #print(feature + " MAE : " + str(mae))
    print(feature + " RMSE : " + str(rmse))
    
if __name__=="__main__":
    print("RANDOM FOREST")
    for feature in featureNames:
        if(feature == "gender" or feature == "age"):
            randomForestClass(feature)
        else:
            randomForestRegr(feature)
