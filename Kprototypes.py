import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from kmodes.kprototypes import KPrototypes
data = pd.read_csv('ProjectData/mergedWatchTime&GenresEncoding.csv')
data = data.replace('\\N',0)
data = data.rename(columns={'\\N':'noGenre'})
data = data.drop(labels='Unnamed: 0',axis = 1)
data = data.fillna(value=0)
popped = data.pop('isAdult')
data['isAdult'] = popped
data.startYear = data.startYear.values.astype(int)
data.runtimeMinutes = data.runtimeMinutes.values.astype(int)
popped = data.pop('startYear')
data['startYear'] = popped
popped = data.pop('averageRating')
data['averageRating'] = popped
popped = data.pop('numVotes')
data['numVotes']= popped
popped = data.pop('runtimeMinutes')
data['runtimeMinutes'] = popped
input = data.iloc[:,7:]
input.iloc[:,:22] = input.iloc[:,:22].astype(int)
input.iloc[:,-4:] = input.iloc[:,-4:].astype(float)
kp = KPrototypes(n_clusters=10, init='Cao', n_init=1, verbose=2)#option are Huang and Cao
clusters = kp.fit_predict(input, categorical=list(range(23)))
data['cluster'] = clusters

data['clusPercent'] = np.zeros(len(data.numVotes.values))
for clusNum in range(10):
    clusData = data.loc[data.cluster==clusNum,:]
    totalLen = len(clusData.startYear.values)
    watchedLen = len(clusData.loc[clusData.watchDate!=0,'originalTitle'])
    data.loc[data.cluster == clusNum,'clusPercent'] = watchedLen/totalLen*100
from sklearn.ensemble import RandomForestRegressor
dataTest = pd.read_csv('ProjectData/testSet.csv')
ranForReg = RandomForestRegressor(random_state=1, n_estimators=10)
ranForReg.fit(input,data.clusPercent)
output=ranForReg.predict(dataTest.iloc[:,8:])
plt.scatter(output,dataTest.index)
for index in range(len(dataTest.index)):
    print(str(dataTest.loc[index,'primaryTitle'])+' has cluster percentage= '+ str(output[index]))
plt.show()






