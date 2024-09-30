import sys
from socket import *

def http_client(server_host, server_port, filename):
    try:
        # Create a TCP socket
        clientSocket=socket(AF_INET, SOCK_STREAM)
        # Establish connection to the server
        clientSocket.connect((server_host, int(server_port)))
        # Form the GET request to be sent to the server
        request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
        # Send the request to the server
        clientSocket.send(request.encode())
        # Receive the response from the server
        response = ""
        while True: # to keep receiving data as long as it is being sent
            # Receive data in chunks of 4096 bytes
            data = clientSocket.recv(4096).decode()
            if not data:
                break
            response += data
        # Print the full server response (headers and content)
        print("Server response:")
        print(response)
        # Close the client socket
        clientSocket.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Correct command is :- python3 client.py server_host server_port filename")
    else:
        # Extract command line arguments
        server_host = sys.argv[1]
        server_port = sys.argv[2]
        filename = sys.argv[3]
        
        # Call the client function
        http_client(server_host, server_port, filename)
