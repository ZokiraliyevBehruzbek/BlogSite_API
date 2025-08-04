from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from pydantic import ValidationError
from blogs.schemas import BlogsSchema, UpdateSchema, UpdateStatus
from models.blogs import Blogs
from models.users import User
from models.category import Category
from core.database import SessionLocal
from core.middlewares import is_admin_user, login_required, is_owner
from models.blogs import ClassType


blog_bp = Blueprint("blog_bp", __name__)


@blog_bp.route("/create", methods=["POST"])
@login_required
def create_products():
    data = request.json
    try:
        blog = BlogsSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session: Session = SessionLocal()
    try:
        user = session.query(User).get(request.user["user_id"])

        if not user:
            return jsonify({"error": "User not found"}), 404

        category = session.query(Category).get(blog.category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        blog = Blogs(
            title=blog.title,
            description=blog.description,
            body=blog.body,
            owner_id=user.id,
            category_id=category.id,
        )
        session.add(blog)
        session.commit()
        return jsonify({"message": "Blog created", "blog_id": blog.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@blog_bp.route("/remove/<int:blog_id>", methods=["DELETE"])
@login_required
@is_owner
def remote_blog(blog_id: int):
    session: Session = SessionLocal()

    try:
        blog = session.query(Blogs).get(blog_id)
        if not blog:
            return jsonify({"error": "Blog not found!"})
        session.delete(blog)
        session.commit()
        return " ", 204
    finally:
        session.close()


@blog_bp.route("/update/<int:blog_id>", methods=["PATCH"])
@login_required
@is_owner
def blog_update(blog_id: int):
    data = request.json

    try:
        updated = UpdateSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session: Session = SessionLocal()
    try:
        blog = session.query(Blogs).get(blog_id)

        if not blog:
            return jsonify({"error": "Blog not found"}), 404

        if updated.title is not None:
            blog.title = updated.title
        if updated.description is not None:
            blog.description = updated.description
        if updated.body is not None:
            blog.body = updated.body

        session.commit()
        return jsonify({"message": "blog updated!"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@blog_bp.route("/status/update/<int:blog_id>", methods=["PATCH"])
@login_required
@is_admin_user
def status(blog_id: int):
    data = request.json
    try:
        status_updated = UpdateStatus(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session: Session = SessionLocal()

    try:
        status = session.query(Blogs).get(blog_id)
        if not status:
            return jsonify({"error": "Blog not found"}), 404
        status.status = status_updated.status
        session.commit()
        return jsonify({"message": "status updated!"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@blog_bp.route("/get/<int:blog_id>", methods=["GET"])
def get_blog(blog_id: int):
    session: Session = SessionLocal()
    try:
        blog = session.query(Blogs).filter(Blogs.id == blog_id, Blogs.status == ClassType.Accepted).one_or_none()
        if blog is None:
            return jsonify({"error": "Blog not found"}), 404

        return (
            jsonify(
                {
                    "id": blog.id,
                    "title": blog.title,
                    "description": blog.description,
                    "body": blog.body,
                    "status": blog.status,
                    "category_id": blog.category_id,
                    "owner_id": blog.owner_id,
                }
            ),
            200,
        )
    finally:
        session.close()


@blog_bp.route("/get/all", methods=["GET"])
def get_all_blogs():
    session: Session = SessionLocal()
    try:
        blogs = session.query(Blogs).filter(Blogs.status == ClassType.Accepted).all()
        if not blogs:
            return jsonify({"error": "No blogs found"}), 404

        return (
            jsonify(
                [
                    {
                        "id": blog.id,
                        "title": blog.title,
                        "description": blog.description,
                        "body": blog.body,
                        "status": blog.status.name,
                        "category_id": blog.category_id,
                        "owner_id": blog.owner_id,
                    }
                    for blog in blogs
                ]
            ),
            200,
        )
    finally:
        session.close()
