import socket  # noqa: F401

def main():
    print("Server is starting...")

    # Create a server socket that would listen on localhost 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221...")

    while True:
        # Wait for a client to connect
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        # Send the HTTP 200 OK response
        response = "HTTP/1.1 200 OK\r\n\r\n"
        client_socket.sendall(response.encode())  # Send the response

        # Close the connection
        client_socket.close()



if __name__ == "__main__":
    main()
