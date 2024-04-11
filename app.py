from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
# from models import db, Toilet

app = Flask(__name__)

# Database
app.config.from_object(Config)
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://mydb.db'
db.init.app(app)

@app.route('/toilets', methods=['GET'])
def get_toilets();
