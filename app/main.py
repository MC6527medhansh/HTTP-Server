import os
import socket  # noqa: F401
import threading
import argparse


def handle_client(client_socket, directory):
    try:
        
        # Receive data from the client socket => get client request
        client_request = client_socket.recv(1024).decode()  # Decode to get string data from bytes
        
        # Extract URL => Get client request line
        try:
            client_request_lines = client_request.split("\r\n")  # Split string into list of lines
            client_request_line = client_request_lines[0]  # First line contains the request line
            method, path, version = client_request_line.split(" ")  # Extract method, path, and version
            print(f"Method: {method}, Path: {path}, Version: {version}")
        except ValueError:
            # If the request is malformed, respond with 400 Bad Request
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
            client_socket.sendall(response.encode())
            return


        # Extract the header lines
        headers = {}
        for line in client_request_lines[1:]:  # Start from the second line and skip the request line
            if ": " in line:  # Check if the line contains a header in 'Key: Value' format
                key, value = line.split(": ", 1)  # Split the line at most once
                headers[key.lower()] = value  # Store the header in lowercase for case insensitivity



        # Handle different paths
        if method == "POST" and path.startswith("/files/"):
            # Handle POST /files/{filename}
            filename = path[len("/files/"):]  # Extract the filename from the path
            file_path = os.path.join(directory, filename)  # Build the full file path
            print(f"POST request to create file: {file_path}")

            # Get Content-Length to determine how much data to read
            content_length = int(headers.get("content-length", 0))
            print(f"Content-Length: {content_length}")

            # Read the request body
            body = client_socket.recv(content_length).decode()  # Read the exact length of the body
            print(f"Request body received: {body}")

            # Write the request body to the specified file
            try:
                with open(file_path, "w") as file:
                    file.write(body)
                print(f"File {file_path} written with contents: {body}")

                # Respond with 201 Created
                response = "HTTP/1.1 201 Created\r\n\r\n"
            except Exception as e:
                print(f"Error writing file: {e}")
                response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
                
        elif path == "/index.html" or path == "/":
            # Send the HTTP 200 OK response
            response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        "Content-Length: 13\r\n\r\n"
                        "Hello, World!"
            )
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
        elif path.startswith("/files/") & method == 'GET':
            # Handle /files/{filename}
            filename = path[len("/files/"):]  # Extract the filename from the path
            file_path = os.path.join(directory, filename)  # Build the full file path

            if os.path.exists(file_path) and os.path.isfile(file_path):  # Check if the file exists
                file_size = os.path.getsize(file_path)  # Get the file size
                with open(file_path, "rb") as file:  # Open the file in binary mode
                    file_contents = file.read()

                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {file_size}\r\n\r\n"
                )
                client_socket.sendall(response.encode() + file_contents)  # Send headers and file contents
            else:
                # File not found
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
                client_socket.sendall(response.encode())
        else:
            # Respond with 404 Not Found
            response = "HTTP/1.1 404 Not Found\r\n\r\nThe requested resource was not found."

        # Send the response
        client_socket.sendall(response.encode())
        
        
        
    except Exception as e:
        print(f"Error handling client: {e}")
        
    finally:
        # Close the connection
        client_socket.close()


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True, help="Directory where files are stored")
    args = parser.parse_args()
    directory = args.directory
    
    print("Server is starting...")
    print(f"Serving files from directory: {directory}")

    # Create a server socket that binds to the address specified and listens on localhost:4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221...")

    while True:
        # Wait for a client to connect
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        # Handle the client in a new thread
        thread = threading.Thread(target=handle_client, args=(client_socket, directory))
        thread.start()


if __name__ == "__main__":
    main()
