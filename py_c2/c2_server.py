#!/bin/python3



from http.server import BaseHTTPRequestHandler as BHTTPR


class C2Handler(BHTTPR):
    """ This is a child class of the BaseHTTPRequestHandler class.
    It handles all HTTP request of our C2 server. """
    
    # noinspection PyPep8Naming
    def do_GET(self):
        # first send back 404 to the client
        self.send_response(404)
        self.end_headers()


