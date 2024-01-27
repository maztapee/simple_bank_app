import json
import sys
from config import app, bank_app_db
from flask import render_template,redirect, url_for, request, jsonify
from datetime import date, datetime, timedelta
from sqlalchemy import func
from model import Customer, Account, Transaction
from sqlalchemy.exc import IntegrityError

#########################################################

# Endpoint to create a user
@app.route('/api/user/create_user', methods=['POST'])
def create_customer():
    data = request.json
    username = data.get('username')
    phone_number = data.get('phone_number')
    email = data.get('email')
    
    # Create the new customer object
    new_customer = Customer(username=username, email=email, phone_number=phone_number)
    bank_app_db.session.add(new_customer)
    bank_app_db.session.commit()  # Commit the new customer to the database to generate the ID
    
    # Retrieve the generated customer ID
    customer_id = new_customer.id
    
    # Generate an account number using customer phone number
    def generate_account_number(phone_number):
        try:
            # Check if the phone number is exactly 11 digits
            if len(phone_number) != 11:
                raise ValueError("Phone number must be 11 digits long")
            
            # Take out the leading number and return the last 10 digits
            return phone_number[1:]
        
        except ValueError as e:
            return str(e)
        except Exception as e:
            return f"An error occurred: {e}"
    account_no = generate_account_number(phone_number)
    
    # Create the new account object
    new_account = Account(account_number=account_no, customer_id=customer_id, balance=0)
    bank_app_db.session.add(new_account)
    bank_app_db.session.commit()  # Commit the new account to the database to generate the ID
    
    # Retrieve the generated account ID
    account_id = new_account.id
    
    # Return the response
    return jsonify({
        'customer_id': customer_id, 
        'username': username,
        'phone_number': phone_number, 
        'email': email,
        'account_id': account_id,
        'account_number': account_no,
        'balance': 0,  # New account balance is initialized to 0
        'message': f"User {username} was successfully created",
    })


# Endpoint to credit a user
@app.route('/api/account/credit_customer', methods=['POST'])
def credit_user():
    data = request.json
    account_number = data.get('account_number')
    amount = data.get('amount')
    
    acct_no = Account.query.get(account_number)
    if acct_no:
        acct_no.balance += amount
        bank_app_db.session.commit()
        return jsonify({
            'balance': acct_no.balance,
            'message': f"Account number {account_number} was successfully credited with {amount}"
            })
    else:
        return jsonify({'message': 'Account number not found'})

# Endpoint to debit a user
@app.route('/api/account/debit_customer', methods=['POST'])
def debit_user():
    data = request.json
    account_number = data.get('account_number')
    amount = data.get('amount')
    
    acct_no = Account.query.get(account_number)
    if acct_no:
        if acct_no.balance >= amount:
            acct_no.balance -= amount
            bank_app_db.session.commit()
            return jsonify({'balance': acct_no.balance})
        else:
            return jsonify({'message': 'Insufficient funds'})
    else:
        return jsonify({'message': 'Account number not found'})

# Endpoint to delete a resource
@app.route('/api/delete/resource-type/id', methods=['DELETE'])
def delete_resource():
    resource_type = request.args.get('resource_type')
    resource_id = request.args.get('id')
    
    # Implement resource deletion logic based on resource_type and resource_id
    # Example: if resource_type == 'user', delete user with id == resource_id
    
    return jsonify({'status': True, 'code': 200, 'message': 'Resource deleted successfully'})

# Endpoint to get list of all customers
@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customer_list = []
    for customer in customers:
        customer_data = {
            'id': customer.id,
            'username': customer.username,
            'phone_number': customer.phone_number,
            'email': customer.email
        }
        customer_list.append(customer_data)
    return jsonify({'customers': customer_list})

# Endpoint to get list of all accounts
@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    account_list = []
    for account in accounts:
        account_data = {
            'account_id': account.id,
            'account_number': account.account_number,
            'balance': account.balance
        }
        account_list.append(account_data)
    return jsonify({'customers': account_list})

# Endpoint to get all transactions of a given account_number/account_id in an array format
@app.route('/api/transactions/<account_identifier>', methods=['GET'])
def get_transactions_by_account(account_identifier):
    # Determine if account_identifier is an account_number or account_id
    if account_identifier.isdigit():
        # Assuming account_identifier is an account_id
        transactions = Transaction.query.filter_by(account_id=int(account_identifier)).all()
    else:
        # Assuming account_identifier is an account_number
        account = Account.query.filter_by(account_number=account_identifier).first()
        if not account:
            return jsonify({'message': 'Account not found'}), 404
        transactions = Transaction.query.filter_by(account_id=account.id).all()

    transaction_list = []
    for transaction in transactions:
        transaction_data = {
            'id': transaction.id,
            'customer_id': transaction.customer_id,
            'account_id': transaction.account_id,
            'type': transaction.type,
            'date': transaction.date.strftime('%d-%m-%Y'),  # Convert date to string format
            'amount': transaction.amount
        }
        transaction_list.append(transaction_data)
    return jsonify({'transactions': transaction_list})

# Endpoint to get all accounts a customer using a customer_id 
@app.route('/api/account/get_by_customer_id/<int:customer_id>', methods=['GET']) 
# api/account/get_by_customer_id/?customer_id=1
def get_account_by_customer_id(customer_id):
    # Implementation using http Request Body/Payload
        # data = request.json
        # customer_id = data.get('customer_id')
        # Use an IF to check for valid customer_id before the try/catch block
    try:
        customer = Customer.query.get_or_404(customer_id)
        accounts = Account.query.filter_by(customer_id=customer_id).all()
        account_list = []
        for account in accounts:
            account_data = {
                'id': account.id,
                'account_number': account.account_number,
                'customer_id': account.customer_id,
                'balance': account.balance
            }
            account_list.append(account_data)
        return jsonify({'customer': {'customer_id': customer.id, 'username': customer.username}, 'accounts': account_list})
    except IntegrityError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
