from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models.base_model import SessionLocal
from services.user_service import (
    add_user_service,
    list_users_service,
    get_user_service,
    update_user_service,
    delete_user_service,
)
from serializers.user_serializer import UserCreate, UserUpdate, UserResponse
from pydantic import ValidationError

user_bp = Blueprint("user", __name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_bp.route("/", methods=["POST"])
def create_user():
    db = next(get_db())
    try:
        data = request.get_json()
        user_data = UserCreate(**data)
        user = add_user_service(db, user_data)
        return jsonify(UserResponse.from_orm(user).dict()), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@user_bp.route("/", methods=["GET"])
def list_users():
    db = next(get_db())
    users = list_users_service(db)
    return jsonify([UserResponse.from_orm(user).dict() for user in users]), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = next(get_db())
    user = get_user_service(db, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(UserResponse.from_orm(user).dict()), 200


@user_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    db = next(get_db())
    try:
        data = request.get_json()
        updates = UserUpdate(**data)
        user = update_user_service(db, user_id, updates)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(UserResponse.from_orm(user).dict()), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = next(get_db())
    user = delete_user_service(db, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200
