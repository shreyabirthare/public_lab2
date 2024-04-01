import json
import threading
import requests
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import csv

CATALOG_PORT = 8081
CATALOG_FILE = "catalog.csv"
LOCK = threading.Lock()
host='localhost'
# Public catalog dictionary
catalog = {}

# Function to load catalog data from disk
def load_catalog():
    global catalog
    with LOCK:
        try:
            with open(CATALOG_FILE, 'r') as file:
                reader = csv.DictReader(file)
                catalog = {row['name']: {'price': float(row['price']), 'quantity': int(row['quantity'])} for row in reader}
        except FileNotFoundError:
            # If the file does not exist, initialize the catalog with default values
            catalog = {
                "Tux": {"price": 15.99, "quantity": 100},
                "Fox": {"price": 12.99, "quantity": 50},
                "Python": {"price": 20.99, "quantity": 75}
            }
            # Save the initial catalog to a new file
            with open(CATALOG_FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['name', 'price', 'quantity'])
                writer.writeheader()
                for name, details in catalog.items():
                    writer.writerow({'name': name, 'price': details['price'], 'quantity': details['quantity']})

# Function to handle product query requests
def handle_query(product_name):
    with LOCK:
        
        if product_name in catalog:
            return catalog[product_name], 200
        else:
            return None, 404

# Function to handle buy requests
def handle_buy(order_data):
    global catalog
    product_name = order_data.get("name")
    quantity = order_data.get("quantity")
    
    if not product_name or not quantity:
        print("product not found/bad req")
        return 400
    
    with LOCK:
        if product_name in catalog and catalog[product_name]['quantity'] >= quantity:
            print("product is in stock, updating catalog")
            catalog[product_name]['quantity'] -= quantity  # Deduct the purchased quantity from the catalog
            # Update the quantity in the catalog CSV file
            # Update the quantity in the catalog CSV file
            with open(CATALOG_FILE, 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            # Find the row corresponding to the product name and update its quantity
            for row in rows:
                if row['name'] == product_name:
                    row['quantity'] = str(int(row['quantity']) - int(quantity))
                    break

            # Write the modified rows back to the CSV file
            with open(CATALOG_FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['name', 'price', 'quantity'])
                writer.writeheader()
                writer.writerows(rows)
               
            return 200
        else:
            return 404

# Catalog Request Handler
class CatalogRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        product_name = parsed_path.path.split("/")[-1]
        product_info, response_code = handle_query(product_name)
        self.send_response(response_code)
        if product_info:
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            product_response = json.dumps(product_info)      #json.dumps(response_data).encode('utf-8')
            self.wfile.write(product_response.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))#.decode('utf')
        #print(f"Raw response for buy query: {post_data.text}")
        response_code = handle_buy(post_data)
        self.send_response(response_code)

        if response_code == 200:
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Order processed successfully"}).encode('utf-8'))
        else:
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Order failed: {response_code}".encode('utf-8'))

# Start the catalog service
def start_catalog_service():
    load_catalog()  # Load the catalog data
    catalog_server = ThreadingHTTPServer((host,CATALOG_PORT), CatalogRequestHandler)
    print(f'Starting catalog service on port {CATALOG_PORT}...')
    catalog_server.serve_forever()

if __name__ == "__main__":
    start_catalog_service()
