import socket

HOST = "127.0.0.1"
PORT = 8080

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server is now listening on {HOST}:{PORT} 👂🏾")

    try:
        while True:
            communication_socket, address = server_socket.accept()
            print(f"Connected to {address}")

            handle_client(communication_socket, address)
    except KeyboardInterrupt: # when stopped with ctrl+c
        print("\nServer shutting down ✌🏾")
    finally:
        server_socket.close()


def handle_client(client_socket, client_address):
    request_text = client_socket.recv(1024).decode("utf-8")
    print("Raw request:")
    print(request_text)

    if not request_text:
        client_socket.close()
        return

    request_line = get_request_line(request_text)
    
    parts = parse_request_line(request_line)
    if not parts:
        response = "HTTP/1.1 400 Bad Request\r\n\r\nBad Request\r\n"
    else:
        method, path, http_version = parts

        print(f"Method: {method}")
        print(f"Path: {path}")
        print(f"Version: {http_version}")

        response = build_response(path)
    
    client_socket.send(response.encode("utf-8"))
    client_socket.close()



def get_request_line(request_text):
    request_lines = request_text.split("\r\n")
    request_line = request_lines[0]

    return request_line


def parse_request_line(request_line):
    parts = request_line.split(" ")
    if len(parts) != 3:
        return None
    else:
        method, path, http_version = parts

    return method, path, http_version


def build_response(path):
    body = f"Requested path: {path}\r\n"
    response = f"HTTP/1.1 200 OK\r\n\r\n{body}"

    return response


if __name__ == "__main__":
    run_server()