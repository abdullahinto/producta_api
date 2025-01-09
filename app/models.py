from pymongo import MongoClient
from app.config import Config
from marshmallow import Schema, fields, validate, ValidationError

client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]

products_collection = db["products"]

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    description = fields.Str(validate=validate.Length(min=1))

    

