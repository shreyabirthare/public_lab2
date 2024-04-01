import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import threading
import requests
import os

FRONT_END_PORT = int(os.getenv('FRONTEND_LISTENING_PORT',12500))
CATALOG_PORT = int(os.getenv('CATALOG_PORT',12501))
ORDER_PORT = int(os.getenv('ORDER_PORT',12502))

FRONTEND_HOST = os.getenv('FRONTEND_HOST', 'localhost')
CATALOG_HOST = os.getenv('CATALOG_HOST', 'localhost')
ORDER_HOST = os.getenv('ORDER_HOST', 'localhost')

class FrontendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Thread ID {threading.get_ident()} handling request from {self.client_address}")
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path.startswith("/products/"):
            product_name = parsed_path.path.split("/")[-1]
            product_info = requests.get(f"http://{CATALOG_HOST}:{CATALOG_PORT}/{product_name}")
            print("raw res:",product_info.text)
            if product_info.status_code==200:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"data": product_info.json()}).encode('utf-8'))
            elif product_info.status_code==404:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                error_message = {"error": {"code": 404, "message": "product not found"}}
                self.wfile.write(json.dumps(error_message).encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                error_message = {"error": {"code": 400, "message": "bad request"}}
                self.wfile.write(json.dumps(error_message).encode('utf-8'))

    def do_POST(self):
        print(f"Thread ID {(threading.get_ident())} handling request from {self.client_address}")
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path.startswith("/orders/"):
            order_data = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
            try:
                order_info = requests.post(f"http://{ORDER_HOST}:{ORDER_PORT}/orders", json=order_data)
                if order_info.status_code==200:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"data": order_info.json()}).encode('utf-8'))
                elif order_info.status_code==404:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    error_message = {"error": {"code": 404, "message": "product not found or is out of stock"}}
                    self.wfile.write(json.dumps(error_message).encode('utf-8'))
            except:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                error_message = {"error": {"code": 400, "message": "bad request"}}
                self.wfile.write(json.dumps(error_message).encode('utf-8'))

# host = 'localhost'
host = FRONTEND_HOST
port = FRONT_END_PORT

frontend_server = ThreadingHTTPServer((host, port), FrontendHandler)

print(f'Starting front-end server on {host}:{port}...')
frontend_server.serve_forever()