import socket  # noqa: F401


def main():
    print("Server is starting...")

    # Create a server socket that binds to the address specified and
    # would listen on localhost 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221...")

    while True:
        # Wait for a client to connect
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        
        # Recieve data from the client socket => get client request
        client_request = client_socket.recv(1024).decode()  # decode to get string data from bytes
        
        # Extract URL => Get client request line
        try:
            client_request_lines = client_request.split("\r\n")  # split string into list to pick individual parts
            client_request_line = client_request[0]  # first line contains request line from where 
            method, path, version = client_request_line.split(" ")  # you extract the method, path and version
            print(f"Method: {method}, Path: {path}, Version: {version}")
        except ValueError:
            # If the request is malformed then respond with 400 Bad Request
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
            client_socket.sendall(response.encode())
            client_socket.close()
            continue
            
        # Extract the header line
        headers = [] 
        for line in client_request_lines[1:]:  # Start from the second line and skip the request line
            if ":" in line:  # Check if the line contains a header in 'Key: Value' format
                key, value = line.split(": ", 1)  # Split the line at most 1 time by using ": "
                headers[key.lower()] = value  # Store the header in lowercase for case insensitivity
        
        if path == "/index.html":
            # Send the HTTP 200 OK response
            response = "HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo/"):
            # Extract string after "/echo/"
            echo_string = path[len("/echo/"):]
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {len(echo_string)}\r\n\r\n"
                f"{echo_string}"
            )
        elif path == "/user-agent":
            user_agent = headers.get("user-agent", "")
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {len(user_agent)}\r\n\r\n"
                f"{user_agent}"
            )
        else:
            # Respond with 404 Not Found
            response = "HTTP/1.1 404 Not Found\r\n\r\nThe requested resource was not found."
            
        client_socket.sendall(response.encode())  # Send the response

        # Close the connection
        client_socket.close()


if __name__ == "__main__":
    main()
