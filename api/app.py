from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Set up CORS for the entire app
CORS(app)


@app.route('/')
def index():
    return 'Hello, World!', 200


@app.route('/api/v1/create_link_token')
def create_link_token():
    return 'Hello, World Token', 200
