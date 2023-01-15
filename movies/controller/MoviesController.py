from flask import render_template, redirect, url_for, request, abort, jsonify
from werkzeug.utils import secure_filename
import os
import datetime
import requests
import json
import logging

from model.Movies import Movies, db
from model.Casting import Casting

URL_ACTORS = "http://localhost:8080/actors"


def log_event(event, id, title):
    if not os.path.exists('logfile.txt'):
        os.makedirs(os.path.dirname('logfile.txt'), exist_ok=True)
        open('logfile.txt', 'w').close()
    with open('logfile.txt', 'a') as f:
        f.write(f'{datetime.datetime.now()} - {event} - id: {id} - title: {title}\n')


def get_all_movies():
    keyword = request.args.get('keyword')
    genre = request.args.get('filter_genre')
    page = request.args.get('page', 1, type=int)
    per_page = 9
    query = Movies.query
    if keyword:
        query = query.filter(Movies.title.ilike(f"%{keyword}%"))
    if genre:
        query = query.filter(Movies.genre == genre)
    num_pages = query.count() // per_page
    if query.count() % per_page > 0:
        num_pages += 1
    movies = query.order_by(Movies.year.desc()).limit(per_page).offset((page - 1) * per_page).all()
    return render_template('movies.html', movies=movies, page=page, pages=num_pages)


def get_all_movies_json():
    movies = Movies.query.all()
    return jsonify([e.serialize() for e in movies])


def get_movie_by_id(id):
    movie = Movies.query.filter_by(id=id).first()
    log_event('GET', id, movie.title)
    if movie is None:
        abort(404)
    actors = requests.get(URL_ACTORS).json()
    filtered_actors = [
        {
            **actor,
            'audience_rating': db.session.query(Casting.audience_rating).filter(Casting.actor_id == actor['id']).filter(
                Casting.movie_id == id).scalar()
        }
        for actor in actors if
        (db.session.query(Casting).filter(Casting.actor_id == actor['id']).filter(Casting.movie_id == id).count() > 0)
    ]
    print(filtered_actors)
    return render_template('movieDetails.html', movie=movie, actors=filtered_actors)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        year = request.form['year']
        rating = request.form['rating']
        file = request.files['poster']
        if file.filename == '':
            return 'No selected file'
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(file.filename)
            id = db.session.execute(db.select([db.func.nextval('movie_id_seq')])).scalar() + 1

            filepath = os.path.join('/var/www/images', f"movie{id}.{filename.rsplit('.', 1)[1].lower()}")
            file.save(filepath)
            imageURL = "http://localhost/" + f"movie{id}.{filename.rsplit('.', 1)[1].lower()}"
            # save the movie to the database
            movie = Movies(title=request.form['title'], genre=request.form['genre'], year=request.form['year'],
                           rating=request.form['rating'], image=imageURL)
            db.session.add(movie)
            db.session.commit()
            log_event('POST', movie.id, movie.title)
            return redirect('/movies')
        else:
            return 'Invalid file format'
        movie = Movies(title=title, genre=genre, year=year, rating=rating, image=image)
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


def delete_movie(id):
    movie = Movies.query.filter_by(id=id).first()
    if movie is None:
        abort(404)
    filepath = os.path.join('/var/www/images', f"movie{id}.{movie.image.rsplit('.', 1)[1].lower()}")
    os.remove(filepath)
    Movies.query.filter_by(id=id).delete()
    db.session.commit()
    log_event('DELETE', id, movie.title)
    return jsonify({'success': True}), 200


def edit_movie(id):
    movie = Movies.query.filter_by(id=id).first()
    if movie is None:
        abort(404)
    if request.method == 'PUT':
        data = request.json
        movie.title = data['title']
        movie.genre = data['genre']
        movie.year = data['year']
        movie.rating = data['rating']
        movie.image = data['image']
        db.session.commit()
        log_event('PUT', id, movie.title)
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)


def edit_page(id):
    movie = Movies.query.filter_by(id=id).first()
    if movie is None:
        abort(404)
    return render_template('edit.html', movie=movie)
