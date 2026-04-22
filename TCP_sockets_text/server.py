import socket

# hosting => local IP address
# connecting => private IP address

# automatically get private ip address like this, but if using virtual box you will get that IP address
host = socket.gethostbyname(socket.gethostname())

HOST = "192.168.12.206" # to avoid getting virtual box IP address, can input private IP addrs manually
LOCAL_HOST = "localhost" # if hosting on this computer only, can also specify local host

PORT = 8080

# socket for running the server, listening for new connections and accepting 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((LOCAL_HOST, PORT)) 

# Listen for incoming connections
server.listen(5)

while True:
    # returns address of client that is connecting and a socket that we can use to talk to that client. 
    # socket to communicate with clients
    communication_socket, address = server.accept() # try/except
    print(f"Connected to {address}")
    
    message = communication_socket.recv(1024).decode("utf-8")
    print(f" Message from client is: {message}")
    
    communication_socket.send(f"Got your message! Thank you!".encode("utf-8"))
    
    communication_socket.close()
    print(f"Connection with {address} ended.")