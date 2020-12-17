from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager
from resources.treks import trek
from resources.user import user
import models

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD" 
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(trek, origins=['http://localhost:8000', '*'], supports_credentials=True) 

CORS(user, origins=['http://localhost:3000', '*'], supports_credentials=True)

app.register_blueprint(user, url_prefix='/user')

app.register_blueprint(trek, url_prefix='/api/v1/treks')

@app.route('/')
def index():
    return 'working'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)