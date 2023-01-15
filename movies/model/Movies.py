from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(120), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'year': self.year,
            'rating': self.rating,
            'image': self.image
        }




