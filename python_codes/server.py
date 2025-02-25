import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an address and port
server_socket.bind(('0.0.0.0', 45689))

# Enable the server to accept connections
server_socket.listen(5)

print("Server listening on port 45689...")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print("Connection from "+str(client_address)+" has been established!")

    # Receive the message from the client
    message = client_socket.recv(1024).decode('utf-8')  # Buffer size of 1024 bytes
    print("Received message: "+str(message))

    # Close the client connection after receiving the message
    client_socket.close()

