from flask import request, jsonify
from app.models.transaction import Transaction
from app.extensions import db
from app.models.category import Category

# Add Transaction
def add_transaction():
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
    
    # Validate transaction_type
    if transaction_type not in ['income', 'expense']:
        return jsonify({"message": "Invalid transaction type"}), 422
    
    # # Check if the category_id exists (no need to filter by user_id anymore)
    # category = Category.query.filter_by(id=category_id).first()
    # if not category:
    #     return jsonify({"message": "Invalid category ID"}), 400

    new_transaction = Transaction(
        date=date,
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
    transactions = Transaction.query.all()  # Removed user_id filtering

    result = []
    for txn in transactions:
        result.append({
            "id": txn.id,
            "date": txn.date.strftime("%Y-%m-%d"),
            "amount": txn.amount,
            "transaction_type": txn.transaction_type,
            "category": txn.category,
            "description": txn.description
        })

    return jsonify(result), 200

# Update Transaction
def update_transaction(transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id).first()

    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404

    data = request.get_json()

    transaction.date = data.get('date', transaction.date)
    transaction.amount = data.get('amount', transaction.amount)
    transaction.transaction_type = data.get('transaction_type', transaction.transaction_type)
    transaction.category_id = data.get('category_id', transaction.category_id)
    transaction.description = data.get('description', transaction.description)

    db.session.commit()

    return jsonify({"message": "Transaction updated successfully"}), 200

# Delete Transaction
def delete_transaction(transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id).first()

    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted successfully"}), 200
