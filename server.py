import socket

HOST = "127.0.0.1"
PORT = 8080

# ========================
# SERVER SETUP
# ========================
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP internet socket
    server_socket.bind((HOST, PORT)) # for hosting (server)
    server_socket.listen(1)

    print(f"Server is now listening on {HOST}:{PORT} 👂🏾")

    try:
        while True:
            communication_socket, address = server_socket.accept() 
            print(f"Connected to {address}")
            handle_client(communication_socket)       
    except KeyboardInterrupt: 
        print("\nServer shutting down ✌🏾")
    finally:
        server_socket.close()


# ========================
# CONNECTION HANDLING
# ========================
def handle_client(client_socket):
    """Processes an incoming HTTP request from a single client connection."""

    request_text = client_socket.recv(1024).decode("utf-8") # decode data from socket using UTF-8
    print("Raw request:")
    print(request_text)

    if not request_text:
        client_socket.close()
        return

    request = parse_request(request_text)
    if request is None:
        response = build_response(400, "Bad Request")
    else:
        path = request["path"]
        file_path = resolve_requested_path(path)
        file_contents = read_file(file_path)

        if file_contents is None:
            response = build_response(404, "<h1>404 Not Found</h1>")
        else:
            response = build_response(200, file_contents)
    
    client_socket.send(response.encode("utf-8")) # encode response using UTF-8
    client_socket.close()


# ========================
# REQUEST PARSING
# ========================
def parse_request(request_text):
    lines = request_text.split("\r\n")
    request_line = lines[0]

    parts = request_line.split(" ")
    if len(parts) != 3:
        return None
    else:
        method, path, http_version = parts
    
    return {
        "method": method,
        "path": path,
        "http_version": http_version,
    }


# ========================
# PATH RESOLUTION
# ========================
def resolve_requested_path(path):
    """Convert URL to file path."""
    if path == "/":
        path = "/index.html"
    
    return "www" + path


# ========================
# FILE HANDLING
# ========================
def read_file(file_path):
    """Read file if it exists, otherwise signals 404."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


# ========================
# RESPONSE BUILDING
# ========================
def build_response(status_code, body):
    if status_code == 200:
        status_line = "HTTP/1.1 200 OK"
    elif status_code == 404:
        status_line = "HTTP/1.1 404 Not Found"
    else:
        status_line = "HTTP/1.1 400 Bad Request"
    
    headers = "Content-Type: text/html"

    return f"{status_line}\r\n{headers}\r\n\r\n{body}"


if __name__ == "__main__":
    run_server()