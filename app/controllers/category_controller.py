from flask import request, jsonify
from app.models.category import Category
from app.extensions import db

# Add Category
def add_category():
    data = request.get_json()

    name = data.get('name')

    if not name:
        return jsonify({"message": "Category name is required"}), 400

    # Check if the category already exists (no need to filter by user_id anymore)
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({"message": "Category already exists"}), 400

    new_category = Category(name=name)

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category added successfully"}), 201

# Get Categories
def get_categories():
    categories = Category.query.all()  # No need to filter by user_id

    result = [{"id": cat.id, "name": cat.name} for cat in categories]

    return jsonify(result), 200
