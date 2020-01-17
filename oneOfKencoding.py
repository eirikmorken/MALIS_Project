import csv
import pandas as pd


#Reading in netflix files and processed IMDB csv file.

filterList = ["Season", "SEASON", "Series", "Fate/Apocrypha", "Top Gear:", "Stranger Things:", "Spartacus: Blood and Sand",
 "Spartacus: Vengeance","Fullmetal Alchemist:","Sword Art Online", "American Horror Story", "Psycho-Pass", "The Seven Deadly Sins", 
 "Deadman Wonderland", "Trollhunters: Tales", "LAST HOPE", "Disenchantment: P", "Avatar: The Last", "Manhunt Unabomber", "Kakegurui",
 "Money Heist:", "SWORDGAI", "HERO MASK", "Love, Death &", "The OA", "Dear White People: Vol", "KENGAN", "Ascension:"]


def readNetflixLocalData(fileIn,fileOut):
    result = []
    with open(fileIn) as textfile:
        newFile = open(fileOut, "w")
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

netflixLocalData = readNetflixLocalData("ProjectData/NetflixViewingHistory.csv","ProjectData/cleanedNetflixFile.txt")
confirmationData = readNetflixLocalData("ProjectData/confirmationNetflixData.csv","ProjectData/cleanedComfirmationData.txt")
#newWatched = ['marriage story', 'The Irishman', 'Terminator Genisys', '6 Underground']
#newUnwathced = ['Christmas wedding planner', 'Rumor has it', 'Kick', 'Manchester by the sea', 
#'HeartBreaker', 'in a valley of violence', 'back of the net', 'locked out', 'The great challenge', 'Ghost stories']

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
poppedMoviesWithNoVotes2 = []
for n in range(len(imdbTable)):
    if imdbTable[n][-1] != "":
        poppedMoviesWithNoVotes.append(imdbTable[n])
        poppedMoviesWithNoVotes2.append(imdbTable[n])
imdbTable = poppedMoviesWithNoVotes
imdbTable2 = poppedMoviesWithNoVotes2

def mergeWatchTime(netflixData):
    #Adding column for mergin 
    for x in range(len(imdbTable)):
        imdbTable[x].append('\\N')
    mergeList = []
    for mov in imdbTable:
        for nflix in netflixData:    
            if nflix [0] == mov[2] or nflix [0] == mov[3]:
                mov[-1] = nflix[1]
                
        mergeList.append(mov)
    return mergeList



def mergeConformationData(netflixData):
    #Adding column for mergin 
    for x in range(len(imdbTable2)):
        imdbTable2[x].append('\\N')
    mergeList = []
    for mov in imdbTable2:
        for nflix in netflixData:
            if nflix [0] == mov[2] or nflix [0] == mov[3]:
                #print(mov)
                mov[-1] = nflix[1]
                mergeList.append(mov)
    return mergeList

#mergedNewWatched = mergeWatchTime(newWatched)
#mergedNewUnwatched = mergeWatchTime(newUnwathced)
#print(mergedNewWatched)
#print(mergedNewUnwatched)


mergedConfirmationData = mergeConformationData(confirmationData)
mergedWatchTimeList = mergeWatchTime(netflixLocalData)
#mergeWatchTimeList = pd.read_csv('ProjectData/cleanedData.csv')
mergedWatchTimeList.pop(0)


#genres_set = set()
#for n in range(len(mergedWatchTimeList)):
#    mov_genres = mergedWatchTimeList[n][8].split(",")
#    mergedWatchTimeList[n][8] = mov_genres[0]
#    for j in range(len(mov_genres)):
#        genres_set.add(mov_genres[j])


df2 = pd.DataFrame(data=mergedConfirmationData)
df2.columns = ['tconst','titleType','primaryTitle','originalTitle','isAdult','startYear','endYear','runtimeMinutes','genres','averageRating','numVotes','watched','watchDate']
genresDf2 = df2['genres'].str.get_dummies(sep=',')
merged2 = pd.concat([df2,genresDf2],axis='columns')
print(merged2)
#merged2.to_csv('ProjectData/corformationDataMerged.csv')


df = pd.DataFrame(data=mergedWatchTimeList)
df.columns = ['tconst','titleType','primaryTitle','originalTitle','isAdult','startYear','endYear','runtimeMinutes','genres','averageRating','numVotes','watched','watchDate',]
genresDf = df['genres'].str.get_dummies(sep=',')
merged = pd.concat([df,genresDf],axis='columns')
#print(merged)
merged.to_csv('ProjectData/mergedWatchTime&GenresEncoding2.csv')
#get df 0
#merged3 = pd.concat([df,df2])