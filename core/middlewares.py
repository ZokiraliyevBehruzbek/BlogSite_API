from functools import wraps
from flask import request, jsonify

from core.database import SessionLocal
from models.users import User
from models.blogs import Blogs
from utils.jwt import verify_access


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]
        try:
            user = verify_access(token)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        # Inject the user into the request context
        request.user = user
        print("User >>>>>>>>", request.user)
        return f(*args, **kwargs)

    return decorated_function


def is_admin_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session = SessionLocal()
            user = (
                session.query(User).get(request.user["user_id"])
            )
            print("User >>>>>>>>", user)
            print(not user, user.is_superuser)
            if not user.is_superuser or not user:
                return jsonify({"error": "Admin access required"}), 403
        except Exception as e:
            return jsonify({"error": "Invalid user or token"}), 401

        # User is admin, continue to the view
        return f(*args, **kwargs)

    return decorated_function


# def is_owner(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         try:
#             session = SessionLocal()
#             user = session.query(User).get(request.user["user_id"])
#             if not user:
#                 return jsonify({"error": "User not found"}), 404

#             # Check if the user is the owner of the resource
#             if user.id != kwargs.get('user_id'):
#                 return jsonify({"error": "You are not the owner of this resource"}), 403
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#         return f(*args, **kwargs)

#     return decorated_function


def is_owner(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header required"}), 401
        
        token = auth_header.split(" ")[1]
        try:
            payload = verify_access(token)
            user_id = payload.get("user_id")
            if not user_id:
                return jsonify({"error": "Invalid token: no user_id"}), 403

            blog_id = kwargs.get("blog_id")
            session = SessionLocal()
            blog = session.query(Blogs).get(blog_id)
            if not blog:
                return jsonify({"error": "Blog not found"}), 404

            if blog.owner_id != user_id:
                return jsonify({"error": "You are not the owner"}), 403

        except Exception as e:
            return jsonify({"error": str(e)}), 401
        finally:
            session.close()

        return f(*args, **kwargs)
    return decorated_function
