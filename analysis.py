import numpy as np
import pandas as pd
df = pd.read_csv('ProjectData/cleanedData')
hist = pd.read_csv('NetflixViewingHistory.csv', sep=',')
Movies = hist[hist.Title.str.contains('Season|SEASON|Episode|Part|Book|Chapter|Limited Series|Spartacus:|Trailer|MOVIE|Sword Art Online:|Blue Exorcist:|Psycho-Pass:|American Horror Story:|Deadman Wonderland:|Seven Deadly Sins|The Bible|Table:|Sherlock:|Manhunt:|Wanderlust:|Black Mirror|Volume|Land Girls:')==False]

