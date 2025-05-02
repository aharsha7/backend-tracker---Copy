from flask import Blueprint
from app.controllers.transaction_controller import add_transaction, get_transactions,get_transaction_by_id, update_transaction, delete_transaction

transaction_bp = Blueprint('transaction_bp', __name__, url_prefix='/api/transactions')

transaction_bp.route('/post', methods=['POST'])(add_transaction)
transaction_bp.route('/get', methods=['GET'])(get_transactions)
transaction_bp.route('/getById/<int:transaction_id>', methods=['GET'])(get_transaction_by_id)
transaction_bp.route('/put/<int:transaction_id>', methods=['PUT'])(update_transaction)
transaction_bp.route('/delete/<int:transaction_id>', methods=['DELETE'])(delete_transaction)
