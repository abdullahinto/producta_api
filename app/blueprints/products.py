from flask import Blueprint, jsonify, request
from app import products_collection
from bson import json_util
from app.models import ProductSchema, ValidationError
import logging
from app import app

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

products_bp = Blueprint("products", __name__)
product_schema = ProductSchema()

def find_product_by_id(id):
    return products_collection.find_one({'id': id}, {"_id": 0})

@products_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = list(products_collection.find({}, {"_id": 0}))
        app.logger.info("Products retrieved successfully")
        return jsonify(products)
    except Exception as e:
        app.logger.error(f"Error retrieving products: {str(e)}")
        return jsonify({"error": "Error retrieving products"}), 500


@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = find_product_by_id(id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product)
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@products_bp.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.json
        product_data = product_schema.load(data)
        
        last_product = products_collection.find_one(sort=[("id", -1)])
        next_id = (last_product["id"] + 1) if last_product else 1

        new_product = {
            "id": next_id,
            "name": product_data["name"],
            "price": product_data["price"],
            "description": product_data.get("description", "")
        }
        products_collection.insert_one(new_product)
        new_product.pop("_id")
        app.logger.info("Product added") 
        return jsonify(new_product), 201
    except ValidationError as err:
        app.logger.error(f"An error occurred while adding a product: {err}")
        return jsonify(err.messages), 400

@products_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = find_product_by_id(id)
    if not product:
        app.logger.error(f"Product with id {id} not found.")
        return jsonify({"error": "Product not found"}), 404

    try:
        data = request.json
        product_data = product_schema.load(data)
        
        updated_field = {
            "name": product_data["name"],
            "price": product_data["price"],
            "description": product_data.get("description", "")
        }
        products_collection.update_one({"id": id}, {"$set": updated_field})
        updated_product = find_product_by_id(id)
        app.logger.info('Product updated')
        return jsonify(updated_product)
    except ValidationError as err:
        app.logger.error(f"An error occurred while updating a product: {err}")
        return jsonify(err.messages), 400

@products_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = find_product_by_id(id)
    if not product:
        app.logger.error(f"Product with id {id} not found.")
        return jsonify({"error": "Product not found"}), 404

    products_collection.delete_one({'id': id})
    app.logger.info(f'Product with id:{id} deleted')
    return jsonify({"message": "Product deleted"}), 200

@products_bp.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e)}), 500
