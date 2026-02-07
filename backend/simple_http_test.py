import http.server
import socketserver
import threading
import time

def run_simple_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Simple server running at port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Run the server in a thread
    server_thread = threading.Thread(target=run_simple_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Simple server started. Waiting for connections...")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        exit(0)