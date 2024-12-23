from flask import Flask


def create_app():
    """A function to create the flask app"""
    app = Flask(__name__)
    return app
