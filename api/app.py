from flask import Flask, request
from flask_cors import CORS
from api.get_plaid_client import get_plaid_client
import api.plaid_helper
import json

app = Flask(__name__)

# Set up CORS for the entire app
CORS(app)

# Set up an init function to run before the app starts
# This is where we'll initialize the Plaid client


@app.before_first_request
def init_app():
    app.plaid_client = get_plaid_client()


@app.route('/')
def index():
    return 'Hello, World!', 200


@app.route('/api/v1/create_link_token')
def create_link_token():
    try:
        link_token = api.plaid_helper.create_link_token(app.plaid_client)
        # Return a json response with the link token
        return {
            'link_token': link_token,
        }, 200
    except Exception as e:
        error_response = json.loads(e.body)
        return {
            'error': {
                'display_message': error_response.get('display_message'),
                'error_code': error_response.get('error_code'),
                'error_type': error_response.get('error_type'),
            }
        }, 500


@app.route('/api/v1/get_access_token', methods=['POST'])
def get_access_token():
    # Get the public token from the request body
    public_token = request.json['public_token']

    # Exchange the public token for an access token
    try:
        access_token = api.plaid_helper.exchange_public_token(
            app.plaid_client,
            public_token)
        # Return a json response with the access token
        return {
            'access_token': access_token,
        }, 200
    except Exception as e:
        error_response = json.loads(e.body)
        return {
            'error': {
                'display_message': error_response.get('display_message'),
                'error_code': error_response.get('error_code'),
                'error_type': error_response.get('error_type'),
            }
        }, 500
