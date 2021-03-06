import csv


#Globallists
results = []
filterList = ["Season", "SEASON", "Series", "Fate/Apocrypha", "Top Gear:", "Stranger Things:", "Spartacus: Blood and Sand",
 "Spartacus: Vengeance","Fullmetal Alchemist:","Sword Art Online", "American Horror Story", "Psycho-Pass", "The Seven Deadly Sins", 
 "Deadman Wonderland", "Trollhunters: Tales", "LAST HOPE", "Disenchantment: P", "Avatar: The Last", "Manhunt Unabomber", "Kakegurui",
 "Money Heist:", "SWORDGAI", "HERO MASK", "Love, Death &", "The OA", "Dear White People: Vol", "KENGAN", "Ascension:"]


#Reading in netflix files 
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

print(result)
#Method for generally reading csv files
def readTsvFile(tf):
    tsvList = []
    with open(tf) as ratingsFile:
        rd = csv.reader(ratingsFile, delimiter="\t",quotechar='"')
        for row in rd:
            tsvList.append(row)
    return tsvList

#newMovList = readTsvFile('ProjecData/')


#ratings = readTsvFile("ProjectData/title_ratings.tsv") #Ratings

#title_basics = readTsvFile("ProjectData/title_basics.tsv")
#print(len(title_basics))



#For reading and filtering IMDB files
def readAndFilterIMDBdata():
    tsvList = []
    movieList = []
    with open("ProjectData/title_basics.tsv") as ratingsFile:
        rd = csv.reader(ratingsFile, delimiter="\t",quotechar='"')
        for row in rd:
            if row[1] == "movie" or row[1] == "tvMovie":
                movieList.append(row)
    return movieList            


IMDBmovs = readAndFilterIMDBdata()
print("Filtered out movies")


#Joining moivies on title, filtering away obscure movies with identical titles to match netflix data
def joinOnTitle():
    joinedMovs = []
    for mov in result:
        for n in range(len(IMDBmovs)):
            if IMDBmovs[n][2] == mov[0]:
                mostVotes = IMDBmovs[n][2]
                while IMDBmovs[n][2] == IMDBmovs[n+1][2]:
                    
                    mostVotes = max(mostVotes[-1], IMDBmovs[n+1][2][-1])
                    n+=1
                joinedMovs.append(mostVotes)
    return joinedMovs


joinedMovs = joinOnTitle()
print("Joined movies.")


for x in range(10):
 #   print(ratings[x])
    #print(result[x])
    #print(IMDBmovs[x])
    print(joinedMovs[x])







