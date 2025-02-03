# -*- coding: utf-8 -*-
"""Group4 Heart Disease.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vxWSrMGvovLDk9z2mciE-zVA-w8-5hXX
"""

import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

df=pd.read_csv("/content/GROUP 4 heart-disease-cleveland.csv") #Load Data
df

"""# New section"""

df.info()

df.head().style.background_gradient(cmap =sns.cubehelix_palette(as_cmap=True))

fig = px.pie(df, ' diagnosis',color_discrete_sequence=['#491D8B','#7D3AC1','#EB548C','#FF5733','#FEF25F'],title='Data Distribution',template='plotly')

fig.show()

fig = px.box(data_frame=df, x=' diagnosis',y='age',color=' diagnosis',color_discrete_sequence=['#491D8B','#7D3AC1','#EB548C','#FF5733','#FEF25F'],orientation='v')
fig.show()

fig = px.histogram(data_frame=df, x='age',color=' diagnosis',color_discrete_sequence=['#491D8B','#7D3AC1','#EB548C','#FF5733','#FEF25F'],nbins=50)
fig.show()

fig = px.box(data_frame=df, x=' diagnosis',y=' trestbps',color=' diagnosis',color_discrete_sequence=['#491D8B','#7D3AC1','#EB548C','#FF5733','#FEF25F'],orientation='v')
fig.show()

fig = px.histogram(data_frame=df, x=' trestbps',color=' diagnosis',color_discrete_sequence=['#491D8B','#7D3AC1','#EB548C','#FF5733','#FEF25F'],nbins=50)
fig.show()

fig = px.box(data_frame=df, x=' diagnosis',y=' chol',color=' diagnosis',color_discrete_sequence=['#491D8B','#7D3AC1','#EB548C','#FF5733','#FEF25F'],orientation='v')
fig.show()

fig = px.histogram(data_frame=df, x=' chol',color=' diagnosis',color_discrete_sequence=['#491D8B','#7D3AC1','#EB548C','#FF5733','#FEF25F'],nbins=50)
fig.show()

fig = px.scatter(data_frame=df, x=' trestbps',y=' chol'
           ,color=' diagnosis',size='age',template='seaborn',color_discrete_sequence=['#491D8B','#7D3AC1','#EB548C','#FF5733','#FEF25F'],)

fig.update_layout(width=800, height=600,
                  xaxis=dict(color="#BF40BF"),
                 yaxis=dict(color="#BF40BF"))
fig.show()

X = df.iloc[:,:-1].values #Set our training data

y = df.iloc[:,-1].values #We'll use this just for visualization as clustering doesn't require labels

X = pd.DataFrame(X)  # Convert to pandas DataFrame for easier manipulation
string_columns = X.select_dtypes(include='object').columns
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
for col in string_columns:
    X[col] = label_encoder.fit_transform(X[col])

sse = []
for i in range(1,9):
    kmeans = KMeans(n_clusters=i , max_iter=300)
    kmeans.fit(X)
    sse.append(kmeans.inertia_)

fig = px.line(y=sse,template="seaborn",title='Eblow Method')
fig.update_layout(width=800, height=600,
title_font_color="#BF40BF",
xaxis=dict(color="#BF40BF",title="Clusters"),
yaxis=dict(color="#BF40BF",title="SSE"))

kmeans = KMeans(n_clusters = 4, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
clusters = kmeans.fit_predict(X)

import plotly.graph_objects as go

fig = go.Figure()

# Convert X to a NumPy array if it's not already
X_array = X.values if isinstance(X, pd.DataFrame) else X

fig.add_trace(go.Scatter(
    x=X_array[clusters == 0, 0], y=X_array[clusters == 0, 1],
    mode='markers', marker_color='#DB4CB2', name='Diagnosis 0'  # Changed name for clarity
))

fig.add_trace(go.Scatter(
    x=X_array[clusters == 1, 0], y=X_array[clusters == 1, 1],
    mode='markers', marker_color='#c9e9f6', name='Diagnosis 1'
))

fig.add_trace(go.Scatter(
    x=X_array[clusters == 2, 0], y=X_array[clusters == 2, 1],
    mode='markers', marker_color='#7D3AC1', name='Diagnosis 2'
))

fig.add_trace(go.Scatter(
    x=X_array[clusters == 3, 0], y=X_array[clusters == 3, 1],
    mode='markers', marker_color='#FEF25F', name='Diagnosis 3'
))

fig.add_trace(go.Scatter(
    x=kmeans.cluster_centers_[:, 0], y=kmeans.cluster_centers_[:, 1],
    mode='markers', marker_color='#CAC9CD', marker_symbol=4, marker_size=13, name='Centroids'
))

fig.update_layout(template='plotly_dark', width=1000, height=500, title='Kmean Clustering Results')
fig.show()

"""**PCA**"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
# %matplotlib inline

df.head()

features = ['age', ' trestbps',
            ' chol']

x = df.loc[:, features].values
x = StandardScaler().fit_transform(x)

y = df.loc[:,[' diagnosis']].values

x = StandardScaler().fit_transform(x)

pd.DataFrame(data = x, columns = features).head()

"""## PCA Projection to 2D"""

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])
principalDf.head(5)

df[[' diagnosis']].head()

finalDf = pd.concat([principalDf, df[[' diagnosis']]], axis = 1)
finalDf.head(5)



"""## Visualize 2D Projection"""

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 Component PCA', fontsize = 20)


diagnosises = [0,1,2,3]
colors = ['r', 'g', 'b', 'y']
for target, color in zip(diagnosises,colors):
    indicesToKeep = finalDf[' diagnosis'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(diagnosises)
ax.grid()

"""## Explained Variance"""

pca.explained_variance_ratio_

