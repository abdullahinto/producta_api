from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables from .env file

class Config:
    DEBUG = True
    MONGO_URI = os.getenv("MONGO_URI", "your_default_uri")
    DB_NAME = os.getenv("DB_NAME", "ecomerce")


