# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from numpy import genfromtxt, savetxt
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.tree import DecisionTreeRegressor,DecisionTreeClassifier
from sklearn.svm import SVR
from math import sqrt
from sklearn.cross_decomposition import PLSRegression
from random import shuffle
from sklearn.linear_model import TheilSenRegressor,Ridge,Lasso,ElasticNet,SGDRegressor

targetFeatures = {"gender" : 1, "age" : 0, "ope" : 2, "con" : 3, "ext" : 4, "agr" : 5, "neu" : 6}
#featureNames = ["gender", "age", "ope", "con", "ext", "agr", "neu"]
featureNames = ["ope", "neu", "ext", "agr", "con"]
predAge = []
predGender = []

#userid, gender, age, ope, con, ext, agr, neu, category
accu = 0
pageUser = {}
user = {}
allCategories = []
allUsers = []

def replaceAge(age):
    if age < 25:
        return 1
    elif age < 35:
        return 2
    elif age < 51:
        return 3
    else:
        return 4

def changeToList(data):
    global pageUser
    global categoryCount
    count = 0
    for x in data:
        userId = x[0]
        if(user.get(userId) == None):
            user[userId] = [replaceAge(float(x[1])),float(x[2]),float(x[3]),float(x[4]),float(x[5]),float(x[6]),float(x[7])]
            category = x[9]
            catList = []
            for cat in allCategories:
                if category == cat:
                    catList.append(1)
                else:
                    catList.append(0)
            pageUser[userId] = catList
        else: 
            category = x[9]
            catList = pageUser.get(userId)
            for cat in allCategories:
                index = allCategories.index(cat)
                like = catList[index]
                if category == cat:
                    catList[index] = like+1
                else:
                    continue
            pageUser[userId] = catList
        count+=1
        if(count%10000 == 0):
            print count
                
def getAllData(targetCol):
    target = []
    test = []
    for eachUser in allUsers:
        targetRec = []
        userRec = user.get(eachUser)
        feature = userRec[targetCol]
        targetRec.append(feature)
        target.append(targetRec)
        
        userRecList = pageUser.get(eachUser)
        test.append(userRecList)
    return target, test

def addGenderToFeature(featureData):
    global predGender
    print "addGenderToFeature"
    print len(featureData)
    features = []
    print len(predGender)
    i= 0
    for x in featureData:
        y = predGender[i]
        x.append(y)
        features.append(x)
        i+=1
    print len(features)
    print "------------------"
    return features
        
def randomForestClass(feature):
    global predGender
    targetData,featureData = getAllData(targetFeatures.get(feature))
    cut = int(len(targetData)* 0.8)
    ageCut = int((len(targetData) - cut)*0.8)
    #print cut
    #print feature
    """if(feature == "age"):
        targetData = targetData[cut+1:]
        featureData = addGenderToFeature(featureData[cut+1:])"""

    target = [x for x in targetData[:cut]]
    pageFeatures = [x for x in featureData[:cut]]
    """if(feature == "age"):
        target = [x for x in targetData[:ageCut]]
        pageFeatures = [x for x in featureData[:ageCut]]"""
        #print ageCut
    #print "training data"
    #print len(target)
    #print len(pageFeatures)
    #print pageFeatures.shape

    #Training
    #randForest = RandomForestClassifier(n_estimators=1000, n_jobs = 2)
    #randForest.fit(pageFeatures, target)
    clf = svm.SVC()
    clf.fit(pageFeatures, target)  
    #Testing Data
    trueVal = [x for x in targetData[cut+1:]]
    testFeatures = [x for x in featureData[cut+1:]]
    """if(feature == "age"):
        trueVal = [x for x in targetData[ageCut +1:]]
        testFeatures = [x for x in featureData[ageCut+1:]]"""
    #print "testing data"
    #print len(trueVal)
    #print len(testFeatures)
    #print testFeatures[0]
    
    #featureAccuracy = 0
    #Prediction using Testing Data and find accuracy
    """if(feature == "age"):
        predAge = randForest.predict(testFeatures)
        featureAccuracy = accuracy_score(trueVal, predAge)
    else:
        predGender = randForest.predict(testFeatures)
        featureAccuracy = accuracy_score(trueVal, predGender)"""
    #predFeature = randForest.predict(testFeatures)
    predFeature = clf.predict(testFeatures)
    featureAccuracy = accuracy_score(trueVal, predFeature)
    
    print(feature + " accuracy : " + str(featureAccuracy))
    
def randomForestRegr(feature):
    global accu
    targetData,featureData = getAllData(targetFeatures.get(feature))
    cut = int(len(targetData)* 0.7)
    #print cut

    target = [x for x in targetData[:cut]]
    pageFeatures = [x for x in featureData[:cut]]
    
    #print len(pageFeatures)
    #print pageFeatures.shape

    #Training
    randForest = RandomForestRegressor(n_estimators=10, n_jobs = 2)
    #randForest = PLSRegression(n_components=2)
    #randForest = TheilSenRegressor(random_state=0)
    #randForest = Ridge(alpha=1.0,fit_intercept=True,solver='sag',tol=0.001)
    #randForest = Lasso(alpha = 0.1)
    #randForest = ElasticNet(alpha=1.0, l1_ratio=0.5, fit_intercept=True, normalize=False, precompute=False, warm_start=False, positive=False, random_state=None, selection='cyclic')
    #randForest = SGDRegressor()
    #randForest = SVR(kernel='poly', degree=3, cache_size=7000, epsilon=0.2, gamma='auto')
    randForest.fit(pageFeatures, target)
    #print randForest
    
    #Testing Data
    trueVal = [x for x in targetData[cut+1:]]
    testFeatures = [x for x in featureData[cut+1:]]
    
    #Prediction using Testing Data and find accuracy
    predFeature = randForest.predict(testFeatures)
    rmse = sqrt(mean_squared_error(trueVal, predFeature))
    accu+=rmse
    #mae = mean_absolute_error(trueVal, predFeature)
    #print(feature + " MAE : " + str(mae))
    #print(feature + " RMSE : " + str(rmse))

if __name__ == "__main__":
    #data = genfromtxt(open('E:/GITProjects/profilePageMap.csv','r'),delimiter=',',dtype = str)[1:]
    with open('E:/GITProjects/textFiles/categoryMap.txt','r') as catFile:
        categoryHash = eval(catFile.read())
        catFile.close()
    with open('E:/GITProjects/textFiles/userDict.txt','r') as catFile:
        user = eval(catFile.read())
        catFile.close()
    with open('E:/GITProjects/textFiles/pageUser.txt','r') as catFile:
        pageUser = eval(catFile.read())
        catFile.close()
    allCategories = categoryHash.keys()
    allUsers = user.keys()
    iterations = 0
    noOfRuns = 5
    for feature in featureNames:
        if(feature == "gender" or feature == "age"):
            randomForestClass(feature)
        else:
            while iterations < noOfRuns:
                shuffle(allUsers)
                randomForestRegr(feature)
                iterations+=1
            print feature + " RMSE = " + str((accu)/noOfRuns)
            accu = 0
            iterations = 0
