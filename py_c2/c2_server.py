#!/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8900
BIND_ADDR = ""

class C2Handler(BaseHTTPRequestHandler):
    """ This is a child class of the BaseHTTPRequestHandler class.
    It handles all HTTP request of our C2 server. """
    
    
    # noinspection PyPep8Naming
    def do_GET(self):
        # first send back 404 to the client
        self.send_response(404)
        self.end_headers()

server = HTTPServer((BIND_ADDR, PORT), C2Handler)
server.serve_forever()
# def run(server_class=HTTPServer, handler_class=BHTTPR):
#     server_address = ('', 8900)
#     httpd = server_class(server_address, handler_class)
#     httpd.serve_forever()


