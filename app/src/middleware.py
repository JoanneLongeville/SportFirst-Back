def handle_cors_headers(handler):
    handler.send_header('Access-Control-Allow-Origin', 'http://localhost:8080')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type, Content-Length')
