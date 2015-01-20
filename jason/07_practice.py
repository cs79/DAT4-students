# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 10:53:47 2015

@author: Jason
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import GridSearchCV

source = "../Data/glass.data"

columns = ['id', 'RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe', 'Type']
data = pd.read_csv(source, header = None, names = columns,
                   index_col = 'id')
attributes = ['building_windows_float', 'building_windows_nonfloat', 'vehicle_windows_float',
'containers', 'tableware', 'headlamps'] # Note: no instances of vehicle_windows_nonfloat in dataset
data['Type'] = data['Type'].astype('category')
data['Type'].cat.categories = attributes

X = data.loc[:, 'RI': 'Fe']
y = data.loc[:, 'Type']

# Step 1: Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 4)

# Steps 2, 3, and 4: Test set errors for different values of k
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

knn = KNeighborsClassifier(n_neighbors=2)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

knn = KNeighborsClassifier(n_neighbors=8)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

# Steps 5 and 6: Apply best model, k = 1, to all data
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X, y)

# Cross validation
scores = cross_val_score(knn, X, y, cv = 5, scoring = 'accuracy')
scores
np.mean(scores)

# Search for optimal value of k
k_range = range(1, 30)
scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores.append(np.mean(cross_val_score(knn, X, y, cv = 5, scoring = 'accuracy')))
    
plt.figure()
plt.plot(k_range, scores)

# Automatic grid search for optimal K
knn = KNeighborsClassifier()
k_range = range(1, 30, 2)
param_grid = dict(n_neighbors=k_range)
grid = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
grid.fit(X, y)

grid.grid_scores_
grid_mean_scores = [result[1] for result in grid.grid_scores_]
plt.figure()
plt.plot(k_range, grid_mean_scores)
grid.best_score_
grid.best_params_
grid.best_estimator_