from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from fuzzywuzzy import process
import pandas as pd

ratings_data = pd.read_csv('dataset/ratings.csv')
movies_data = pd.read_csv('dataset/movies.csv')

indexies = pd.Series(movies_data.index, index=movies_data['title'])
all_titles = [movies_data['title'][i] for i in range(len(movies_data['title']))]

def find_item_based_movie(movie_name):

    id_movie = process.extractOne(movie_name, movies_data['title'])[2]
    return movies_data['title'][id_movie]

def get_item_based_recommendations(movie_name):
    csr_movie_user = csr_matrix(ratings_data)

    id_movie = process.extractOne(movie_name, movies_data['title'])[2]
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6).fit(csr_movie_user)
    indices = model_knn.kneighbors(csr_movie_user[id_movie], n_neighbors=6, return_distance=False)

    for i in indices:
        list_mov = list(movies_data['title'][i].where(i != id_movie))
        return list_mov