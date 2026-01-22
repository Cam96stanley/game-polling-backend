from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class App(db.Model):
  __tablename__ = "apps"
  
  app_id = db.Column(db.BigInteger, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  last_updated = db.Column(db.DateTime)