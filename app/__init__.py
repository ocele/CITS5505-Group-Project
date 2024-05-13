from flask import Flask
from .routes import configure_routes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    configure_routes(app)

    return app
