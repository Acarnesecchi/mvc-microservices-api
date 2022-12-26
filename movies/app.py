from flask import Flask, render_template
from model.Movies import db
from routes.movies_bp import movies_bp

app = Flask(__name__, template_folder='view')
app.config.from_object('config')

db.init_app(app)

app.register_blueprint(movies_bp, url_prefix='/movies')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
