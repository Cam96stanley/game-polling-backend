from dotenv import load_dotenv
import os

load_dotenv()

DB_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")