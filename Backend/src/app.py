from flask import Flask
from flask_cors import CORS
from .routes import app_register_bp

app = Flask(__name__)

CORS(app)

def configure_blueprints():
    with app.app_context():
        app_register_bp()

configure_blueprints()

if __name__ == "__main__":
    app.run()