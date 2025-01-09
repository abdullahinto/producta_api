from flask import Flask
from app.config import Config
from pymongo import MongoClient


app = Flask(__name__)
app.config.from_object(Config)


# Initialize MongoDB client and database
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["DB_NAME"]]
products_collection = db["products"]
# products_collection.create_index([("name", 1)]) 



from app.blueprints.products import products_bp
app.register_blueprint(products_bp)

from app.blueprints.users import users_bp
app.register_blueprint(users_bp)
