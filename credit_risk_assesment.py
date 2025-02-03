# -*- coding: utf-8 -*-
"""credit risk assesment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rNOY5cE0gqm3N0-am4u7eAT2mF4TJ3j8
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score

from google.colab import drive
drive.mount('/content/drive')

data_dir = '/content/drive/My Drive/credit/'

import os
for dirname, _, filenames in os.walk(data_dir):
    for filename in filenames:
        print(os.path.join(dirname, filename))

df = pd.read_csv('bankloans.csv')
df.head()

df.isnull().sum()

df.value_counts()

df = df.dropna()

fig,ax = plt.subplots(figsize=(20,10))
sns.lineplot(x='age',y='income',data=df,ax=ax)

fig,ax = plt.subplots(figsize=(20,10))
sns.lineplot(x='age',y='debtinc',data=df,ax=ax)

df['default'].value_counts()

x=df.drop(['default'],axis=1)
y=df['default']

xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.2,random_state=42)

sc = StandardScaler()
xtrain=sc.fit_transform(xtrain)
xtest=sc.fit_transform(xtest)

rfc = RandomForestClassifier(n_estimators=200)

rfc.fit(xtrain,ytrain)

rfc.score(xtest,ytest)

rfc2 = cross_val_score(estimator=rfc,X=xtrain,y=ytrain,cv=10)
rfc2.mean()

sv = SVC()
sv.fit(xtrain,ytrain)

sv = SVC()
sv.fit(xtrain,ytrain)

model = GridSearchCV(sv,{
    'C':[0.1,0.2,0.4,0.8,1.2,1.8,4.0,7.0],
    'gamma':[0.1,0.4,0.8,1.0,2.0,3.0],
    'kernel':['rbf','linear']
},scoring='accuracy',cv=10)

model.fit(xtrain,ytrain)

model.best_params_

model2 = SVC(C=0.1,gamma=0.1,kernel='linear')
model2.fit(xtrain,ytrain)
model2.score(xtest,ytest)

lr = LogisticRegression()
lr.fit(xtrain,ytrain)
lr.score(xtest,ytest)

yp = lr.predict(xtest)
c= confusion_matrix(ytest,yp)
fig ,ax = plt.subplots(figsize=(20,10))
sns.heatmap(c,ax=ax)