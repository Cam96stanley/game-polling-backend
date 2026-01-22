import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

load_dotenv()

DB_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
