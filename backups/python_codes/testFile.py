import socket

def send_file(server_ip, server_port, file_path):
    try:
        # Create a TCP/IP socket
        file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the server's IP and port
        file_socket.connect((server_ip, server_port))

        with open(file_path, 'rb') as f:
            print("Sending file"+str(file_path))
            while True:
                chunk = f.read(1024)  # Read file in chunks
                if not chunk:
                    break
                file_socket.sendall(chunk)

        print("File sent successfully.")
        file_socket.shutdown(socket.SHUT_WR)
        
    finally:
        print("Socket closed.")
        file_socket.close()

# Example usage:
send_file('149.161.65.103', 45689, '/home/nao/scripts/tmp/test2.ogg')  # Send file to the server at IP 149.161.65.48

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








