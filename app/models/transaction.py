from app.extensions import db
from app.models.user import User

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False) 
    category_id = db.Column(db.Integer, nullable=False, default=1) 
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, amount, transaction_type, category, date, user_id, description=None):
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.date = date
        self.user_id = user_id
        self.description = description

    def __repr__(self):
        return f'<Transaction id={self.id}, type={self.transaction_type}, amount={self.amount}, date={self.date}>'
