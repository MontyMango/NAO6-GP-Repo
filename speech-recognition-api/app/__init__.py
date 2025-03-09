from flask import Flask
from app.routes import api
import os

def create_app():
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = "upload/"

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])    

    # Register the routes
    app.register_blueprint(api)
    
    return app

app = create_app()