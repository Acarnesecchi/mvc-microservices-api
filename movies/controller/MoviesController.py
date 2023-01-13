from flask import render_template, redirect, url_for, request, abort, jsonify
from werkzeug.utils import secure_filename
import os

from model.Movies import Movies, db


def get_all_movies():
    page = request.args.get('page', 1, type=int)
    per_page = 9
    num_pages = Movies.query.count() // per_page
    if Movies.query.count() % per_page > 0:
        num_pages += 1
    movies = Movies.query.limit(per_page).offset((page - 1) * per_page).all()
    return render_template('movies.html', movies=movies, page=page, pages=num_pages)


def get_movie_by_id(id):
    movie = Movies.query.filter_by(id=id).first()
    if movie is None:
        abort(404)
    return render_template('movieDetails.html', movie=movie)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def create_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        year = request.form['year']
        rating = request.form['rating']
        file = request.files['poster']
        if file.filename == '':
            # If the user did not select a file
            return 'No selected file'
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            # Use the secure_filename function to ensure the file name is safe
            filename = secure_filename(file.filename)
            id = Movies.query.count() + 1
            # Build the file path using the os.path.join function
            filepath = os.path.join('/var/www/images', f"movie{id}.{filename.rsplit('.', 1)[1].lower()}")
            file.save(filepath)
            imageURL = "http://localhost/" + f"movie{id}.{filename.rsplit('.', 1)[1].lower()}"
            # save the movie to the database
            movie = Movies(title=request.form['title'], genre=request.form['genre'], year=request.form['year'],
                          rating=request.form['rating'], image=imageURL)
            db.session.add(movie)
            db.session.commit()
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
    print(movie.title)
    if movie is None:
        abort(404)
    Movies.query.filter_by(id=id).delete()
    db.session.commit()
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
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)


def edit_page(id):
    movie = Movies.query.filter_by(id=id).first()
    if movie is None:
        abort(404)
    return render_template('edit.html', movie=movie)
