from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Casting(db.Model):
    __tablename__ = 'movies_actors_relation'

    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    audience_rating = db.Column(db.Float, nullable=False)

