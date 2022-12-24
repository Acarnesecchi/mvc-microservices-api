from flask import Blueprint

from controller.MoviesController import index, get_all_movies, get_movie_by_id, add_movie, update_movie, delete_movie

movies_bp = Blueprint('movies_bp', __name__)

movies_bp.route('/', methods=['GET'])(index)
movies_bp.route('/movies', methods=['GET'])(get_all_movies)
movies_bp.route('/movies/<int:id>', methods=['GET'])(get_movie_by_id)
movies_bp.route('/create', methods=['POST'])(add_movie)
movies_bp.route('/movies/<int:id>', methods=['PUT'])(update_movie)
movies_bp.route('/movies/<int:id>', methods=['DELETE'])(delete_movie)