# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 16:32:36 2017

@author: DaCapo
"""

import pickle
import numpy as np


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
clf = svm.SVC()
clf.fit(X_train, y_train)
predicted = clf.predict(X_test)
#print float(np.sum(clf.predict(X_test)==y_test))/float(len(y_test))
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))