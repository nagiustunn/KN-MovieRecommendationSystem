import flask
import csv
from flask import Flask, render_template, request
import random
import content_based_filter
import item_based_collaboravite_filter
from item_based_collaboravite_filter import get_item_based_recommendations, find_item_based_movie
from content_based_filter import get_content_based_recommendations, get_content_based_suggestions


app = flask.Flask(__name__, template_folder='templates')

app = Flask(__name__)


@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template("homepage.html")

@app.route("/contentBasedHomepage")
def contentBased():
    NewMovies = []
    with open('movie.csv', 'r') as csvfile:
        readCSV = csv.reader(csvfile)
        NewMovies.append(random.choice(list(readCSV)))
    movie_name = NewMovies[0][0]
    movie_name = movie_name.title()

    with open('movie.csv', 'a', newline='') as csv_file:
        fieldnames = ['Movie']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'Movie': movie_name})
        result_final_movies = get_content_based_recommendations(movie_name)
        names = []
        dates = []
        ratings = []
        overview = []
        types = []
        mid = []
        for i in range(len(result_final_movies)):
            names.append(result_final_movies.iloc[i][0])
            dates.append(result_final_movies.iloc[i][1])
            ratings.append(result_final_movies.iloc[i][2])
            overview.append(result_final_movies.iloc[i][3])
            types.append(result_final_movies.iloc[i][4])
            mid.append(result_final_movies.iloc[i][5])
    movie_suggestions = get_content_based_suggestions()

    return render_template('contentBasedHomepage.html', suggestions=movie_suggestions, movie_type=types[5:],
                           movie_id=mid, movie_overview=overview, movie_names=names,
                           movie_date=dates, movie_ratings=ratings, search_name=movie_name)


@app.route('/contentBasedRecommendation', methods=['GET', 'POST'])
def getRecommendContentBased():
    if flask.request.method == 'GET':
        return (flask.render_template('contentBasedHomepage.html'))

    if flask.request.method == 'POST':
        movie_name = flask.request.form['movie_name']
        movie_name = movie_name.title()
        if movie_name not in content_based_filter.all_titles:
            return (flask.render_template('error.html', name=movie_name))
        else:
            with open('movie.csv', 'a', newline='') as csv_file:
                fieldnames = ['Movie']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerow({'Movie': movie_name})
            result_final_movies = get_content_based_recommendations(movie_name)
            names = []
            dates = []
            ratings = []
            overview = []
            types = []
            mid = []
            for i in range(len(result_final_movies)):
                names.append(result_final_movies.iloc[i][0])
                dates.append(result_final_movies.iloc[i][1])
                ratings.append(result_final_movies.iloc[i][2])
                overview.append(result_final_movies.iloc[i][3])
                types.append(result_final_movies.iloc[i][4])
                mid.append(result_final_movies.iloc[i][5])


            return flask.render_template('contentBasedRecommendation.html', movie_type=types[5:], movie_id=mid,
                                         movie_overview=overview, movie_names=names, movie_date=dates,
                                         movie_ratings=ratings, search_name=movie_name)


@app.route('/itemBasedHomepage')
def itemBased():
    return render_template("itemBasedHomepage.html")


@app.route('/itemBasedRecommendation', methods=['POST'])
def getRecommendItemBased():
    movie_name = request.form['movie']

    if movie_name not in item_based_collaboravite_filter.all_titles:
        return (flask.render_template('itemBasederror.html', name=movie_name))
    else:
        find_movie = find_item_based_movie(movie_name)
        recommendation_movie = get_item_based_recommendations(movie_name)

    return render_template("itemBasedRecommendation.html", movie=find_movie, rec_movie=recommendation_movie)

if __name__ == '__main__':
    app.run()