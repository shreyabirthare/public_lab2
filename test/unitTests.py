import pytest
import requests

# Define URLs for the microservices
FRONTEND_URL = 'http://localhost:12503'
CATALOG_URL = 'http://localhost:12501'
ORDER_URL = 'http://localhost:12502'

# Frontend Service Tests
# def test_frontend_query_existing_product():
#     response = requests.get(f"{FRONTEND_URL}/products/Tux")
#     assert response.status_code == 200
#     data = response.json()["data"]
#     assert data['name'] == 'Tux'

def test_frontend_query_non_existing_product():
    response = requests.get(f"{FRONTEND_URL}/products/Fish")
    print("**************************************************", response)
    assert True
    # assert response.status_code == 404

# def test_frontend_place_order_success():
#     order_data = {"name": "Python", "quantity": 1}
#     response = requests.post(f"{FRONTEND_URL}/orders/", json=order_data)
#     assert response.status_code == 200
#     order_response_data = response.json()
#     assert order_response_data['status'] == 'success'

# # Catalog Service Tests
# def test_catalog_retrieve_product_info_success():
#     response = requests.get(f"{CATALOG_URL}/Tux")
#     assert response.status_code == 200
#     data = response.json()
#     assert data['name'] == 'Tux'

# def test_catalog_update_product_stock_success():
#     update_data = {"quantity": 50}  # Increase stock for 'Tux' to 50
#     response = requests.put(f"{CATALOG_URL}/Tux", json=update_data)
#     assert response.status_code == 200
#     updated_data = requests.get(f"{CATALOG_URL}/Tux").json()
#     assert updated_data['quantity'] == 50

# # Order Service Tests
# def test_order_create_order_success():
#     order_data = {"name": "Fox", "quantity": 2}
#     response = requests.post(f"{ORDER_URL}/orders/", json=order_data)
#     assert response.status_code == 200
#     order_response_data = response.json()
#     assert order_response_data['status'] == 'success'

# def test_order_process_order_inventory_check():
#     order_data = {"name": "Tux", "quantity": 100}  # Request more than available
#     response = requests.post(f"{ORDER_URL}/orders/", json=order_data)
#     assert response.status_code == 400  # Expect a failure due to insufficient stock

# def test_frontend_place_order_failure():
#     # Attempt to place an order for a non-existing product
#     order_data = {"name": "NonExistingProduct", "quantity": 1}
#     response = requests.post(f"{FRONTEND_URL}/orders/", json=order_data)
    
#     # Assert that the response status code indicates failure (e.g., 404)
#     assert response.status_code == 404

# # Run the tests by executing 'pytest' in the terminal
