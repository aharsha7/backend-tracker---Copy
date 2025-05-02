from flask import Blueprint
from app.controllers.category_controller import add_category, get_categories

category_bp = Blueprint('category_bp', __name__, url_prefix='/api/categories')

category_bp.route('/add', methods=['POST'])(add_category) 
category_bp.route('/', methods=['GET'])(get_categories)
