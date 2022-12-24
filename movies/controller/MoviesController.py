import sys
from flask import render_template, redirect, url_for, request, abort

from model.Movies import Movies

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def index():
    return render_template('index.html')

def get_all_movies():
    movies = Movies.query.all()
    return render_template('movies.html', movies=movies)

def get_movie_by_id(id):
    movie = Movies.query.filter_by(id=id).first()
    if movie is None:
        abort(404)
    return render_template('movie.html', movie=movie)

def add_movie():
    title = request.form['title']
    genre = request.form['genre']
    year = request.form['year']
    rating = request.form['rating']
    movie = Movies(title=title, genre=genre, year=year, rating=rating)
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for('movies_bp.get_all_movies'))

def update_movie(id):
    movie = Movies.query.filter_by(id=id).first()
    if movie is None:
        abort(404)
    movie.title = request.form['title']
    movie.genre = request.form['genre']
    movie.year = request.form['year']
    movie.rating = request.form['rating']
    db.session.commit()
    return redirect(url_for('movies_bp.get_all_movies'))

def delete_movie(id):
    movie = Movies.query.filter_by(id=id).first()
    if movie is None:
        abort(404)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('movies_bp.get_all_movies'))

