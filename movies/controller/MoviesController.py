from flask import render_template, redirect, url_for, request, abort

from model.Movies import Movies


def get_all_movies():
    movies = Movies.query.all()
    movieList = [movie.serialize for movie in movies]
    return render_template('movies.html', movies=movieList)


def get_movie_by_id(id):
    movie = Movies.query.filter_by(id=id).first()
    if movie is None:
        abort(404)
    return render_template('movies.html', movie=movie)


