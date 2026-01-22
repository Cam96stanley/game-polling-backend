from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class App(db.Model):
  __tablename__ = "apps"
  
  app_id = db.Column(db.BigInteger, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  last_updated = db.Column(db.DateTime)
  
class AppPrice(db.Model):
  __tablename__ = "app_price"
  
  app_id = db.Column(db.BigInteger, primary_key=True)
  price = db.Column(db.Integer, nullable=False)
  last_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())