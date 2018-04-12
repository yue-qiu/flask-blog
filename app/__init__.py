import config
from .main import main
from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    bootstrap.init_app(app)

    app.register_blueprint(main)

    return app