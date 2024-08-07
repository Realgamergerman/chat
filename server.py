from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Speicher für Nachrichten
messages = []

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        elif self.path == '/messages':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode())
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == '/messages':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            new_message = json.loads(post_data)
            messages.append(new_message)
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_message).encode())
        else:
            self.send_error(404, "File not found")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=7654):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
