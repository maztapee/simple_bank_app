from config import bank_app_db

class Customer(bank_app_db.Model):
    id = bank_app_db.Column(bank_app_db.Integer, primary_key=True, autoincrement=True)
    username = bank_app_db.Column(bank_app_db.String(50), nullable=False)
    phone_number = bank_app_db.Column(bank_app_db.String(20), unique=True, nullable=False)
    email = bank_app_db.Column(bank_app_db.String(120), unique=True, nullable=False)

class Account(bank_app_db.Model):
    id = bank_app_db.Column(bank_app_db.Integer, primary_key=True, autoincrement=True)
    account_number = bank_app_db.Column(bank_app_db.String(20), unique=True, nullable=False)
    customer_id = bank_app_db.Column(bank_app_db.Integer, bank_app_db.ForeignKey('customer.id'), nullable=False)
    balance = bank_app_db.Column(bank_app_db.Float, default=0.0)
    customer = bank_app_db.relationship('Customer', backref=bank_app_db.backref('accounts', lazy=True))

class Transaction(bank_app_db.Model):
    id = bank_app_db.Column(bank_app_db.Integer, primary_key=True, autoincrement=True)
    customer_id = bank_app_db.Column(bank_app_db.Integer, bank_app_db.ForeignKey('customer.id'), nullable=False)
    account_id = bank_app_db.Column(bank_app_db.Integer, bank_app_db.ForeignKey('account.id'), nullable=False)
    type = bank_app_db.Column(bank_app_db.String(10), nullable=False)  # Debit or Credit
    date = bank_app_db.Column(bank_app_db.Date, nullable=False)
    amount = bank_app_db.Column(bank_app_db.Float, nullable=False)
    customer = bank_app_db.relationship('Customer', backref=bank_app_db.backref('transactions', lazy=True))
    account = bank_app_db.relationship('Account', backref=bank_app_db.backref('transactions', lazy=True))