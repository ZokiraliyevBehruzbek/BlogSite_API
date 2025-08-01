from flask import Blueprint, request, jsonify
from category.handlers import (
    create_category,
    get_all_categories,
    get_category_by_id,
    update_category,
    delete_category,
)
from category.schemas import WriteCategorySchema

category_bp = Blueprint("category", __name__)

# ✅ CREATE
@category_bp.route("/create", methods=["POST"])


def category_create():
    data = request.get_json()
    try:
        validated = WriteCategorySchema(**data)
        category = create_category(validated.name)
        return jsonify({"xabar": "Kategoriya muvaffaqiyatli yaratildi", "id": category.id}), 201
    except Exception as e:
        return jsonify({"xato": str(e)}), 400

# ✅ LIST ALL
@category_bp.route("/all", methods=["GET"])

def list_categories():
    categories = get_all_categories()
    return jsonify([{"id": c.id, "nomi": c.name} for c in categories]), 200

# ✅ GET BY ID
@category_bp.route("/<int:category_id>", methods=["GET"])

def get_category(category_id):
    category = get_category_by_id(category_id)
    if not category:
        return jsonify({"xato": "Kategoriya topilmadi"}), 404
    return jsonify({"id": category.id, "nomi": category.name}), 200

# ✅ UPDATE
@category_bp.route("/update/<int:category_id>", methods=["PUT"])
def update_category_route(category_id):
    data = request.get_json()
    try:
        validated = WriteCategorySchema(**data)
        category = update_category(category_id, validated.name)
        if not category:
            return jsonify({"xato": "Kategoriya topilmadi"}), 404
        return jsonify({
            "xabar": "Kategoriya muvaffaqiyatli yangilandi",
            "id": category.id
        }), 200
    except Exception as e:
        return jsonify({"xato": str(e)}), 400


# ✅ DELETE
@category_bp.route("/delete/<int:category_id>", methods=["DELETE"])
def delete_category_route(category_id):
    result = delete_category(category_id)
    if not result:
        return jsonify({"xato": "Kategoriya topilmadi"}), 404
    return jsonify({"xabar": "Kategoriya muvaffaqiyatli o‘chirildi"}), 200