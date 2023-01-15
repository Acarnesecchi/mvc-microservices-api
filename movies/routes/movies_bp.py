from flask import Blueprint

from controller.MoviesController import get_all_movies, get_movie_by_id, delete_movie, create_movie, edit_page, edit_movie, get_all_movies_json

movies_bp = Blueprint('movies_bp', __name__)

movies_bp.route('/', methods=['GET'])(get_all_movies)
movies_bp.route('/<int:id>', methods=['GET'])(get_movie_by_id)
movies_bp.route('/edit/<int:id>', methods=['GET'])(edit_page)
movies_bp.route('/create', methods=['GET', 'POST'])(create_movie)
movies_bp.route('/<int:id>', methods=['DELETE'])(delete_movie)
movies_bp.route('/<int:id>', methods=['PUT'])(edit_movie)
movies_bp.route('/json', methods=['GET'])(get_all_movies_json)
