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

def get_transaction_by_id(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)

    return jsonify({
        'id': transaction.id,
        'amount': transaction.amount,
        'transaction_type': transaction.transaction_type,
        'category': transaction.category,
        'description': transaction.description,
        'date': transaction.date.isoformat() if transaction.date else None
    })

def update_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid JSON input'}), 400

    transaction.amount = data.get('amount', transaction.amount)
    transaction.transaction_type = data.get('transaction_type', transaction.transaction_type)
    transaction.description = data.get('description', transaction.description)

    # Category handling
    category_name = data.get('category')
    if category_name:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            # auto-create category if not exists
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()  # commit to get the ID
        transaction.category_id = category.id

    # Date parsing (optional)
    date_str = data.get('date')
    if date_str:
        from datetime import datetime
        try:
            transaction.date = datetime.fromisoformat(date_str)
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    db.session.commit()

    return jsonify({'message': 'Transaction updated successfully'})

# Delete Transaction
def delete_transaction(transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id).first()

    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted successfully"}), 200
