import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import threading
import requests
FRONTEND_PORT = 8080

class FrontendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Thread ID {threading.get_ident()} handling request from {self.client_address}")
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path.startswith("/products/"):
            product_name = parsed_path.path.split("/")[-1]
            product_info = requests.get(f"http://localhost:8081/{product_name}")
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
                order_info = requests.post("http://localhost:8082/orders", json=order_data)
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

host = 'localhost'
port = 8080

frontend_server = ThreadingHTTPServer((host, port), FrontendHandler)

print(f'Starting front-end server on {host}:{port}...')
frontend_server.serve_forever()