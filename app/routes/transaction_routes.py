from flask import Blueprint
from app.controllers.transaction_controller import add_transaction, get_transactions, update_transaction, delete_transaction

transaction_bp = Blueprint('transaction_bp', __name__, url_prefix='/api/transactions')

# No longer using jwt_required() since JWT is removed for these routes
transaction_bp.route('/', methods=['POST'])(add_transaction)
transaction_bp.route('/', methods=['GET'])(get_transactions)
transaction_bp.route('/<int:transaction_id>', methods=['PUT'])(update_transaction)
transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])(delete_transaction)
