import http.server, socketserver, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8770
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"serving on http://127.0.0.1:{PORT}")
    httpd.serve_forever()
