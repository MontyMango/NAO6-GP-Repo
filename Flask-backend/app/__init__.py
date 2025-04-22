from flask import Flask
from flask_cors import CORS
from app.routes import api

import os

def create_app():
    app = Flask(__name__)

    # This enables CORS for the flask backend server
    # So we can recieve input from our frontend on all routes.
    CORS(app)

    app.config['UPLOAD_FOLDER'] = "upload/"

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])    

    # Register the routes
    app.register_blueprint(api)
    
    return app

app = create_app()