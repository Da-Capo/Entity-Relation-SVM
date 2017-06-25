# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 16:32:36 2017

@author: DaCapo
"""

import pickle
import numpy as np
import matplotlib as plt


def softmax(x):
    x -=  np.max(x,axis=-1,keepdims=True)
    x = np.exp(x)/np.sum(np.exp(x),axis=-1,keepdims=True)
    return x

def computsx(sx, alpha):
    prex = np.argmax(sx,axis=1)
    sxx = sx > alpha
    scc = np.sum(sxx,axis=1)
    return metrics.f1_score(y_test[scc>0], prex[scc>0], average="micro")
#    print(metrics.classification_report(y_test[scc>0], prex[scc>0]))

with open('feature.pkl', 'rb') as f:
    data = pickle.load(f)

from sklearn import svm
from sklearn import preprocessing
from sklearn import metrics


X  = np.array([x[0] for x in data["features"].values()])
y  = np.array([x[1] for x in data["features"].values()])


X_scaled  = preprocessing.scale(X)

#np.random.choice(5, 3)
X_train = X_scaled[:8000]
y_train = y[:8000]
X_test = X_scaled[8000:]
y_test = y[8000:]
print "初始化"
clf = svm.SVC(probability=True, decision_function_shape="ovr")
print "训练中"
clf.fit(X_train, y_train)
predicted = clf.predict(X_test)
#clf.predict_proba(X_test)
#print float(np.sum(clf.predict(X_test)==y_test))/float(len(y_test))
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))
sx = softmax(clf.decision_function(X_test))
#sx /= np.max(sx,axis=-1,keepdims=True)

f1_s = []
for i in range(1,100):
    alpha = i/100.0
    f1_s.append(computsx(sx, alpha))
    
