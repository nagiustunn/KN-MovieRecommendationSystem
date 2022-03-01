import pandas as pd

import matplotlib.pyplot as plt


movies = pd.read_csv('movie_dataset/movie.csv')
movies.head(10)

movies['genres'] = movies['genres'].str.replace('|',' ')

counts = dict()
for i in movies.index:
   for g in movies.loc[i,'genres'].split(' '):
      if g not in counts:
         counts[g] = 1
      else:
         counts[g] = counts[g] + 1
# create a bar chart
plt.bar(list(counts.keys()), counts.values(), color='g')
plt.xticks(rotation=45)
plt.xlabel('Genres')
plt.ylabel('Counts')
plt.show()