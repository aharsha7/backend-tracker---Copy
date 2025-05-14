from flask import request, jsonify
from app.models.transaction import Transaction
from app.extensions import db
from app.models.category import Category
from datetime import datetime
import jwt

# Add Transaction
def add_transaction():
    user_id, error_response, status = get_user_id_from_token()
    if error_response:
        return error_response, status

    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    date = data.get('date')
    amount = data.get('amount')
    transaction_type = data.get('transaction_type')
    category = data.get('category')
    description = data.get('description')

    if not all([date, amount, transaction_type, category]):
        return jsonify({"message": "Missing required fields"}), 400

    if transaction_type not in ['income', 'expense']:
        return jsonify({"message": "Invalid transaction type"}), 422

    try:
        date_obj = datetime.fromisoformat(date)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    new_transaction = Transaction(
        user_id=user_id,
        date=date_obj,
        amount=amount,
        transaction_type=transaction_type,
        category=category,
        description=description
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added successfully"}), 201

# Get Transactions
def get_transactions():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header missing or invalid"}), 401

    token = auth_header.split("Bearer ")[1]
    try:
        decoded = jwt.decode(token, "app123", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    user_id = decoded.get('id')
    if not id:
        return jsonify({"error": "Invalid token payload"}), 401

    transactions = Transaction.query.filter_by(user_id=user_id).all()

    result = [{
        "id": txn.id,
        "date": txn.date.strftime("%Y-%m-%d"),
        "amount": txn.amount,
        "transaction_type": txn.transaction_type,
        "category": txn.category,
        "description": txn.description
    } for txn in transactions]

    return jsonify(result), 200

# Get User by ID
def get_user_id_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, jsonify({"error": "Authorization header missing or invalid"}), 401

    token = auth_header.split("Bearer ")[1]
    try:
        decoded = jwt.decode(token, "app123", algorithms=["HS256"])
        user_id = decoded.get('id')
        if not user_id:
            return None, jsonify({"error": "Invalid token payload"}), 401
        return user_id, None, None
    except jwt.ExpiredSignatureError:
        return None, jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return None, jsonify({"error": "Invalid token"}), 401

#Get transaction by Id
def get_transaction_by_id(transaction_id):
    user_id, error_response, status = get_user_id_from_token()
    if error_response:
        return error_response, status

    # Example query (adjust according to your models)
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    # Serialize transaction (adjust fields as needed)
    transaction_data = {
        "id": transaction.id,
        "amount": transaction.amount,
        "transaction_type": transaction.transaction_type,
        "category": transaction.category,
        "description": transaction.description,
        "date": transaction.date.isoformat()
    }

    return jsonify(transaction_data), 200
    
# Update Transaction
def update_transaction(transaction_id):
    user_id, error_response, status = get_user_id_from_token()
    if error_response:
        return error_response, status

    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return jsonify({"error": "Transaction not found or unauthorized"}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON input'}), 400

    transaction.amount = data.get('amount', transaction.amount)
    transaction.transaction_type = data.get('transaction_type', transaction.transaction_type)
    transaction.description = data.get('description', transaction.description)

    category_name = data.get('category')
    if category_name:
        transaction.category = category_name

    date_str = data.get('date')
    if date_str:
        from datetime import datetime
        try:
            transaction.date = datetime.fromisoformat(date_str)
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    db.session.commit()

    return jsonify({'message': 'Transaction updated successfully'}), 200

# Delete Transaction
def delete_transaction(transaction_id):
    user_id, error_response, status = get_user_id_from_token()
    if error_response:
        return error_response, status

    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return jsonify({"error": "Transaction not found or unauthorized"}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted successfully"}), 200
