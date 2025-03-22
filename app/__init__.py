from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    os.makedirs("temp_storage", exist_ok=True)

    from .routes import main
    app.register_blueprint(main)

    return app
