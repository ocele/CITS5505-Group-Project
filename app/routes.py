# def configure_routes(app):
#     @app.route('/')
#     def home():
#         return "Welcome to the Flask App!"

from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')
