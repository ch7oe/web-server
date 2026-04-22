import socket

# IP of the server to send requests to. 
# Running on same computer, so same as local IP address
HOST = "192.168.12.206"
LOCAL_HOST = "localhost"

PORT = 8080

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((LOCAL_HOST, PORT)) # sends a request to server. server has to accept request 

socket.send("HELLO WORLD!".encode("utf-8"))
print(socket.recv(1024).decode("utf-8"))

