from flask import Flask
from app.utils.logger import setup_logger
import os

def create_app():
    app = Flask(__name__)

    os.makedirs("temp_storage", exist_ok=True)

    app.logger = setup_logger("app_logger")

    from .routes import main
    app.register_blueprint(main)

    app.logger.info("Flask app initialized")

    return app
