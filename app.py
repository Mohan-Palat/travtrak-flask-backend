from flask import Flask, jsonify, g
from flask_cors import CORS
from resources.treks import trek
import models

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

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

CORS(trek, origins=['http://localhost:8000', '*'], supports_credentials=True) # adding this line

app.register_blueprint(trek, url_prefix='/api/v1/treks') # adding this line

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'working'


# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)