from flask import Flask, render_template
from flask_migrate import Migrate

from model.Movies import db
from routes.movies_bp import movies_bp

app = Flask(__name__, template_folder='view')
app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(movies_bp, url_prefix='/movies')


@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	app.debug = True
	app.run()
	app.template_folder = '/movies/view/'

