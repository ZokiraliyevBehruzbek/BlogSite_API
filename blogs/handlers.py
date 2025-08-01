from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from pydantic import ValidationError
from blogs.schemas import BlogsSchema
from models.blogs import Blogs
from models.users import User
from core.database import SessionLocal
from core.middlewares import login_required, is_owner



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
        user = session.query(User).get(request.user["user_id"]) # type: ignore
        if not user:
            return jsonify({"error": "User not found"}), 404

        # category = session.query(Category).get(blog.category_id) # type: ignore
        # if not category:
        #     return jsonify({"error": "Category not found"}), 404

        blog = Blogs(
            title=blog.title,
            description=blog.description,
            body=blog.body,
            owner_id=user.id,
            # category_id=category.id,
            status=blog.status
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