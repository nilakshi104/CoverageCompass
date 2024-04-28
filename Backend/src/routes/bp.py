from flask import Blueprint, current_app
from flask_restx import Resource, Api

api_blueprint = Blueprint('api', __name__, url_prefix="/covcomp")
api = Api(api_blueprint, title="Status Clain Validation API")

def app_register_bp():
    print("REGISTER BP")
    current_app.register_blueprint(api_blueprint)
    