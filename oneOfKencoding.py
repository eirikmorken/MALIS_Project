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

#Reading 
def readTsvFile(tf):
    tsvList = []
    with open(tf) as ratingsFile:
        rd = csv.reader(ratingsFile, delimiter=",")
        for row in rd:
            tsvList.append(row)
    return tsvList

imdbTable = readTsvFile("ProjectData/cleanedData.csv")


#Removing all IMDB movies with no votes
poppedMoviesWithNoVotes = []
for n in range(len(imdbTable)):
    if imdbTable[n][-1] != "":
        poppedMoviesWithNoVotes.append(imdbTable[n])
imdbTable = poppedMoviesWithNoVotes


def mergeWatchTime():
    #Adding column for mergin 
    for x in range(len(imdbTable)):
        imdbTable[x].append('\\N')
    mergeList = []
    for mov in imdbTable:
        for nflix in netflixLocalData:    
            if nflix [0] == mov[2] or nflix [0] == mov[3]:
                mov[-1] = nflix[1]
                
        mergeList.append(mov)
    return mergeList

mergedWatchTimeList = mergeWatchTime()
#mergeWatchTimeList = pd.read_csv('ProjectData/cleanedData.csv')
mergedWatchTimeList.pop(0)


genres_set = set()
for n in range(len(mergedWatchTimeList)):
    mov_genres = mergedWatchTimeList[n][8].split(",")
    mergedWatchTimeList[n][8] = mov_genres[0]
    for j in range(len(mov_genres)):
        genres_set.add(mov_genres[j])


df = pd.DataFrame(data=mergedWatchTimeList)
df.columns = ['tconst','titleType','primaryTitle','originalTitle','isAdult','startYear','endYear','runtimeMinutes','genres','averageRating','numVotes','watchDate']
genresDf = df['genres'].str.get_dummies(sep=',')
merged = pd.concat([df,genresDf],axis='columns')
print(merged)
#merged.to_csv('ProjectData/mergedWatchTime&GenresEncoding.csv')
