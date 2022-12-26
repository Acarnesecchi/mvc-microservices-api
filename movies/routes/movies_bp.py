from flask import Blueprint

from controller.MoviesController import get_all_movies, get_movie_by_id

movies_bp = Blueprint('movies_bp', __name__)

movies_bp.route('/', methods=['GET'])(get_all_movies)
movies_bp.route('/<int:id>', methods=['GET'])(get_movie_by_id)
