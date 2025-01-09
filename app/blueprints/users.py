from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import app
from flask import Blueprint, jsonify, request
from app.models import  ValidationError



app.config['JWT_SECRET_KEY'] = 'Mangoman908'
jwt = JWTManager(app)

users_bp = Blueprint("users", __name__)

@users_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@users_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200