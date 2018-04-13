import config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet,IMAGES,configure_uploads

bootstrap = Bootstrap()
photos = UploadSet('PHOTOS')

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    bootstrap.init_app(app)

    configure_uploads(app, photos)

    from .main import main
    app.register_blueprint(main)

    return app