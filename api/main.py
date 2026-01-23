import os
from dotenv import load_dotenv
from flask import Flask
from models.app import db

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)

with app.app_context():
  db.drop_all()
  db.create_all()