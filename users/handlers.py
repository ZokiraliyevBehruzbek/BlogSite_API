from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session
from utils.auth import hash_password, verify_password
from utils.jwt import full_jwt
from users.schemas import RegisterSchema, LoginSchema, GetSchema, ResetPasswordSchema
from models.users import User
from core.middlewares import login_required, is_admin_user
from core.database import SessionLocal

user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        validated = RegisterSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session: Session = SessionLocal()
    try:
        user = User(
            username=validated.username,
            email=validated.email,
            password=hash_password(validated.password),
            is_superuser=validated.is_superuser,
        )
        session.add(user)
        session.commit()
        token = full_jwt({"user_id": user.id})
        return jsonify({"message": "Registered", "jwt": token}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        validated = LoginSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session: Session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=validated.username).one_or_none()
        if not user or not verify_password(validated.password, user.password):
            return jsonify({"error": "Invalid credentials"}), 401

        token = full_jwt({"user_id": user.id})
        return jsonify({"jwt": token}), 200
    finally:
        session.close()


@user_bp.route("/get", methods=["POST"])
@login_required
@is_admin_user
def get_user():
    data = request.get_json()
    try:
        validated = GetSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session: Session = SessionLocal()
    try:
        target = session.query(User).get(validated.id)
        if not target:
            return jsonify({"error": "User not found"}), 404

        return (
            jsonify(
                {
                    "id": target.id,
                    "username": target.username,
                    "email": target.email,
                }
            ),
            200,
        )
    finally:
        session.close()



@user_bp.route("/reset-password", methods=["POST"])
@login_required
def reset_password():
    data = request.get_json()
    try:
        reset_pass = ResetPasswordSchema(**data)
        session: Session = SessionLocal()
        try:
            # foydalanuvchini token orqali aniqlaymiz
            user = session.query(User).filter_by(id=request.user["user_id"]).first()

            if not user or not verify_password(reset_pass.old_password, user.password):
                return jsonify({"error": "Invalid credentials"}), 401

            user.password = hash_password(reset_pass.new_password)
            session.commit()

            return jsonify({"message": "Password successfully updated"}), 200
        finally:
            session.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Parol reset qilish api - done