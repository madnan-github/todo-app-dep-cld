# Simple backend for testing
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import sys
from urllib.parse import urlparse

class TaskFlowBackend(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>TaskFlow Backend Running!</h1><p>Backend is operational with Dapr and Kafka integration.</p></body></html>')
        elif parsed_path.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "timestamp": "2026-02-08T17:00:00Z",
                "service": "backend",
                "version": "1.0.0",
                "database": "disconnected",
                "kafka": "disconnected",
                "environment": "development"
            }
            self.wfile.write(json.dumps(response).encode())
        elif parsed_path.path == '/docs':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>API Documentation</h1><p>Swagger UI would be here in the full application.</p></body></html>')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "message": "Request received",
            "path": self.path,
            "data_length": content_length
        }
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, TaskFlowBackend)
    print(f'Starting TaskFlow backend on port {port}...')
    httpd.serve_forever()