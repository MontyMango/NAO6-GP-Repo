import socket

def receive_file(server_ip, server_port, output_file):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the server address and port
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print("Server listening...")

    # Wait for a connection
    connection, client_address = server_socket.accept()
    print("Connection established with "+str(client_address))

    with open(output_file, 'wb') as f:
        print("Receiving file and saving as "+str(output_file))
        while True:
            # Receive data in small chunks
            data = connection.recv(1024)
            if not data:
                break
            f.write(data)

    print("File received successfully.")
    connection.close()

# Example usage:
receive_file('0.0.0.0', 45689, 'received_file.ogg')  # Server listens on port 45689 

