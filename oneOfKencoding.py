import csv
import pandas as pd


#Reading in netflix files and processed IMDB csv file.

filterList = ["Season", "SEASON", "Series", "Fate/Apocrypha", "Top Gear:", "Stranger Things:", "Spartacus: Blood and Sand",
 "Spartacus: Vengeance","Fullmetal Alchemist:","Sword Art Online", "American Horror Story", "Psycho-Pass", "The Seven Deadly Sins", 
 "Deadman Wonderland", "Trollhunters: Tales", "LAST HOPE", "Disenchantment: P", "Avatar: The Last", "Manhunt Unabomber", "Kakegurui",
 "Money Heist:", "SWORDGAI", "HERO MASK", "Love, Death &", "The OA", "Dear White People: Vol", "KENGAN", "Ascension:"]


def readNetflixLocalData():
    result = []
    with open("ProjectData/NetflixViewingHistory.csv") as textfile:
        newFile = open("ProjectData/cleanedNetflixFile.txt", "w")
        next(textfile)
        for line in textfile:
            passedFilter = True
            for f in filterList:
                if f in line:
                    passedFilter = False
            if passedFilter == True:
                newFile.write(line)
                line = line.strip('\"\n').split('","')
                
                result.append(line)
        newFile.close()
    return result

netflixLocalData = readNetflixLocalData()

def readTsvFile(tf):
    tsvList = []
    with open(tf) as ratingsFile:
        rd = csv.reader(ratingsFile, delimiter=",")
        for row in rd:
            tsvList.append(row)
    return tsvList

mainTable = readTsvFile("ProjectData/cleanedData.csv")

#Removing all IMDB movies with no votes
poppedMoviesWithNoVotes = []
for n in range(len(mainTable)):
    if mainTable[n][-1] != "":
        poppedMoviesWithNoVotes.append(mainTable[n])
mainTable = poppedMoviesWithNoVotes




def mergeWatchTime():
    #Adding column for mergin 
    for x in range(len(mainTable)):
        mainTable[x].append('\\N')
    mergeList = []
    for mov in mainTable:
        for nflix in netflixLocalData:    
            if nflix [0] == mov[2] or nflix [0] == mov[3]:
                mov[-1] = nflix[1]
                
        mergeList.append(mov)
    return mergeList

mergedWatchTimeList = mergeWatchTime()
workinglist = mergedWatchTimeList
workinglist.pop(0)
genres_set = set()
for n in range(len(workinglist)):
    mov_genres = workinglist[n][8].split(",")
    workinglist[n][8] = mov_genres[0]
    for j in range(len(mov_genres)):
        genres_set.add(mov_genres[j])

print(len(genres_set))
df = pd.DataFrame(data=workinglist)
df.columns = ['tconst','titleType','primaryTitle','originalTitle','isAdult','startYear','endYear','runtimeMinutes','genres','averageRating','numVotes','watchDate']
genresDf = df['genres'].str.get_dummies(sep=',')


#dummies = pd.get_dummies(df.genres)
#print(dummies)
merged = pd.concat([df,genresDf],axis='columns')
#print(merged)
#print(df)
#for col in merged.columns:
 #   print(col)
merged.to_csv('ProjectData/mergedWatchTime&GenresEncoding.csv')
