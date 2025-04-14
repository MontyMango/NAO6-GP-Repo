import socket

# Server details
server_host = '149.161.65.103'  # Server's IP address (localhost for local server)
server_port = 45689        # Port number where the server is listening

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_host, server_port))

# Define the message or script to send to the server
message = "Hello from python client!"
print("Message sent!")

# Send the script/message to the server
client_socket.sendall(message.encode('utf-8'))

# Optionally, receive a response from the server (if needed)
response = client_socket.recv(1024)  # Buffer size is 1024 bytes
print("Server Response:", response.decode('utf-8'))

# Close the connection
client_socket.close()
