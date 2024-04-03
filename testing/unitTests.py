import requests
import unittest

class FrontEndServiceTest(unittest.TestCase):
    FRONT_END_URL = 'http://localhost:12503'

    def test_query_existing_product(self):
        response = requests.get(f'{self.FRONT_END_URL}/products/Tux')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('name', data['data'])
        self.assertEqual(data['data']['name'], 'Tux')

    # def test_query_non_existing_product(self):
    #     response = requests.get(f'{self.FRONT_END_URL}/products/Crocodile')
    #     data = response.json()
    #     print(data)
    #     self.assertEqual(response.status_code, 404)

class CatalogServiceTest(unittest.TestCase):
    CATALOG_URL = 'http://localhost:12501'

    def test_retrieve_product_info_directly(self):
        response = requests.get(f'{self.CATALOG_URL}/Tux')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'Tux')


#     def test_update_product_quantity_directly(self):
#         response = requests.post(f'{self.CATALOG_URL}/update', json={'name': 'Tux', 'quantity': 10000})
#         self.assertEqual(response.status_code, 200)
#         product_response = requests.get(f'{self.CATALOG_URL}/Tux')
#         self.assertEqual(product_response.status_code, 200)
#         product_data = product_response.json()
#         self.assertEqual(product_data.get('quantity'), 10000)


class OrderServiceTest(unittest.TestCase):
    ORDER_URL = 'http://localhost:12502'

    # def test_place_order_directly(self):
    #     response = requests.post(f'{self.ORDER_URL}/orders', json={'name': 'Fox', 'quantity': 1})
    #     self.assertEqual(response.status_code, 200)
    #     data = response.json()
    #     self.assertIn('order_number', data)
    #     self.assertIn('name', data)
    #     self.assertIn('quantity', data)
    #     self.assertEqual(data['name'], 'Fox')
    #     self.assertEqual(data['quantity'], 1)

    def test_quantity_more_than_available(self):
        response = requests.post(f'{self.ORDER_URL}/orders', json={'name': 'Tux', 'quantity': 500000})
        self.assertNotEqual(response.status_code, 200)
    
    def test_place_order_for_non_existing_product(self):
        response = requests.post(f'{self.ORDER_URL}/orders', json={'name': 'Caterpillar', 'quantity': 1})
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()