import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import requests
import csv
import os

ORDER_PORT = int(os.getenv('ORDER_LISTENING_PORT',12502))
CATALOG_PORT = int(os.getenv('CATALOG_LISTENING_PORT',12501))
ORDER_FILE = "order_data/order_log.csv"
LOCK = threading.Lock()
CATALOG_HOST = os.getenv('CATALOG_HOST', 'localhost')
ORDER_HOST = os.getenv('ORDER_HOST', 'localhost')
host=ORDER_HOST
# host = 'localhost'

# Global variable to store the order number
order_number = 0

# Function to generate a unique order number
def generate_order_number():
    global order_number
    with LOCK:
        order_number += 1
        return order_number - 1  # Return the current order number before incrementing

# Function to log the order in a CSV file
def log_order(order_number, product_name, quantity):
    with LOCK:
        with open(ORDER_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([order_number, product_name, quantity])

# Function to load the order number from the order log CSV file
def load_order_number():
    global order_number
    if os.path.exists(ORDER_FILE) and os.path.getsize(ORDER_FILE) > 0:
        with LOCK:
            with open(ORDER_FILE, 'r') as file:
                reader = csv.reader(file)
                last_row = list(reader)[-1]  # Get the last row from the CSV file
                order_number = int(last_row[0]) + 1  # Increment the order number from the last order
    else:
        order_number = 0

# Order Request Handler
class OrderRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            
            # Send a POST request to the catalog service
            catalog_response = requests.post(f"http://{CATALOG_HOST}:{CATALOG_PORT}/orders", json=post_data)
            print("response code from catalog ",catalog_response.status_code)
            if catalog_response.status_code == 200:
                print("success from catalog side")
                order_number = generate_order_number()
                product_name = post_data.get("name")
                quantity = post_data.get("quantity")
                
                # Log the order in the order log CSV file
                log_order(order_number, product_name, quantity)
                
                # Send the order number back to the frontend service
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response_data = {"order_number": order_number}
                self.wfile.write(json.dumps(response_data).encode())
            else:
                # Send only the error code to the frontend service
                self.send_response(catalog_response.status_code)
                self.end_headers()

# Start the order service
def start_order_service():
    load_order_number()  # Load the order number from the order log CSV file
    order_server = ThreadingHTTPServer((host, ORDER_PORT), OrderRequestHandler)
    print(f'Starting order service on port {ORDER_PORT}...')
    order_server.serve_forever()

if __name__ == "__main__":
    start_order_service()
