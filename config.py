from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_migrate import Migrate

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Maztapee-1989@localhost/simple_bank'
bank_app_db = SQLAlchemy(app)
migrate = Migrate(app, bank_app_db)
