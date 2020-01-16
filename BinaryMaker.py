import pandas as pd
import numpy as np
from kmodes.kmodes import KModes
data = pd.read_csv('ProjectData/mergedWatchTime&GenresEncoding.csv')
data = data.replace('\\N',0)
data = data.rename(columns={'\\N':'noGenre'})
data = data.drop(labels='Unnamed: 0',axis = 1)
data = data.fillna(value=0)
isAdult = data.pop('isAdult')
data['isAdult'] = isAdult
data.startYear = data.startYear.values.astype(int)
data.runtimeMinutes = data.runtimeMinutes.values.astype(int)
data['OaF-release'] = np.ones(len(data.startYear.values))
data.loc[data.startYear>1975,'OaF-release']=0
for i in range(1975,2015,5):
    title = str(i)+'_'+str(i+5)
    data[title] = np.zeros(len(data.startYear.values))
    data.loc[(data.startYear>i)&(data.startYear<=(i+5)),title]=1
data['noVotes'] = np.zeros(len(data.numVotes.values))
data.loc[data.numVotes<=1,'noVotes']=1
for i in range(7):
    title = '10^'+str(i)+'_votes'
    data[title]= np.zeros(len(data.numVotes.values))
    data.loc[(data.numVotes>10**i)&(data.numVotes<=10**(i+1)),title] = 1
data['noRating'] = np.zeros(len(data.averageRating.values))
data.loc[data.averageRating==0,'noRating']=1
for i in range(10):
    title = str(i)+'_rating'
    data[title] = np.zeros(len(data.averageRating.values))
    data.loc[(data.averageRating > i) & (data.averageRating <= (i + 1)), title] = 1
print(data.iloc[:,11:])
data.iloc[:,11:] = data.iloc[:,11:].astype(int)
print(data)

# define the k-modes model
km = KModes(n_clusters=10, init='Huang', n_init=11, verbose=1)
# fit the clusters to the skills dataframe
clusters = km.fit_predict(data.iloc[:,11:])
# get an array of cluster modes
kmodes = km.cluster_centroids_
shape = kmodes.shape
# For each cluster mode (a vector of "1" and "0")
# find and print the column headings where "1" appears.
# If no "1" appears, assign to "no-skills" cluster.
data['cluster'] = clusters

clusterss = data.loc[data.cluster==data.iloc[0,-1],:]
for clusNum in range(11):
    clusData = data.loc[data.cluster==clusNum,:]
    totalLen = len(clusData.startYear.values)
    watchedLen = len(clusData.loc[clusData.watchDate!=0,'originalTitle'])