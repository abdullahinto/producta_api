from app import app

def test_create_product():
    with app.test_client() as client:
        response = client.post('/products', json={
            "name": "Test Product",
            "price": 10.0,
            "description": "This is a test product"
        })
        assert response.status_code == 201
        assert response.json["name"] == "Test Product"
        assert response.json["price"] == 10.0
        assert response.json["description"] == "This is a test product"

def test_create_product_invalid():
    with app.test_client() as client:
        response = client.post('/products', json={
            "name": "Test Product"
        })
        assert response.status_code == 400
        assert 'price' in response.json
        assert response.json['price'] == ['Missing data for required field.']

def test_get_products():
    with app.test_client() as client:
        response = client.get('/products')
        assert response.status_code == 200
        assert isinstance(response.json, list)

        
def test_get_product():
    with app.test_client() as client:
        # Create a product first
        response = client.post('/products', json={
            "name": "Test Product",
            "price": 10.0,
            "description": "This is a test product"
        })
        product_id = response.json['id']

        # Now get the product
        response = client.get(f'/products/{product_id}')
        assert response.status_code == 200
        assert response.json["name"] == "Test Product"
        assert response.json["price"] == 10.0
        assert response.json["description"] == "This is a test product"


def test_update_product():
    with app.test_client() as client:
        response = client.post('/products', json={
            "name": "Test Product",
            "price": 10.0,
            "description": "This is a test product"
        })
        product_id = response.json['id']

        response = client.put(f"/products/{product_id}", json={
            "name": "Updated Product",
            "price": 15.0,
            "description": "This is an updated test product"
        })
        assert response.status_code == 200
        assert response.json["name"] == "Updated Product"
        assert response.json["price"] == 15.0
        assert response.json["description"] == "This is an updated test product"

        response = client.get(f'/products/{product_id}')
        assert response.status_code == 200
        assert response.json["name"] == "Updated Product"
        assert response.json["price"] == 15.0
        assert response.json["description"] == "This is an updated test product"



def test_delete_product():
    with app.test_client() as client:
        # Create a product first
        response = client.post('/products', json={
            "name": "Test Product",
            "price": 10.0,
            "description": "This is a test product"
        })
        product_id = response.json['id']

        # Now delete the product
        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 200
        assert response.json["message"] == "Product deleted"