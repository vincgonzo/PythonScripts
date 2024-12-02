import http.server
import socketserver
import cgi

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Define the length of the body data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Here you can save the post_data to a file or process it
        with open("received_data.txt", "wb") as f:
            f.write(post_data)

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Data received successfully!")

    def do_GET(self):
        # Handle GET requests (optional)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, this is a simple server!")

# Define the server settings
PORT = 9000

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
