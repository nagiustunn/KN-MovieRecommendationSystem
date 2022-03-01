import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movie_data = pd.read_csv("movie_dataset/movie.csv", dtype='object')
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(movie_data['soup'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

movie_data = movie_data.reset_index()
indexies = pd.Series(movie_data.index, index=movie_data['title'])
all_titles = [movie_data['title'][i] for i in range(len(movie_data['title']))]


def get_content_based_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    id_movie = indexies[title]
    similarity_scores = list(enumerate(cosine_sim[id_movie]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:11]
    movie_indices = [i[0] for i in similarity_scores]
    title = movie_data['title'].iloc[movie_indices]
    date = movie_data['release_date'].iloc[movie_indices]
    rating = movie_data['vote_average'].iloc[movie_indices]
    movie_details = movie_data['overview'].iloc[movie_indices]
    movie_types = movie_data['keywords'].iloc[movie_indices]
    movie_id = movie_data['id'].iloc[movie_indices]

    return_df = pd.DataFrame(columns=['Title', 'Year'])
    return_df['Title'] = title
    return_df['Year'] = date
    return_df['Ratings'] = rating
    return_df['Overview'] = movie_details
    return_df['Types'] = movie_types
    return_df['ID'] = movie_id
    return return_df


def get_content_based_suggestions():
    data = pd.read_csv('movie_dataset/movie.csv')
    return list(data['title'].str.capitalize())