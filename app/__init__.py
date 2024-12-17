from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import os


def create_app():
    app = Flask(__name__)

    SWAGGER_URL = '/swagger'
    API_URL = '/swagger/swagger.yaml'

    # Setup Swagger UI
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Flask Solid Login API"
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/swagger/swagger.yaml')
    def swagger_yaml():
        return send_from_directory(os.path.join(app.root_path, 'swagger'), 'swagger.yaml')

    return app
