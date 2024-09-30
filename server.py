#import socket module
from socket import *
import sys  # In order to terminate the program
import threading  # threading module for handling multiple clients

# Function to handle individual client requests
def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()  # Receive and decode the client's request
        
        # Check if the message is empty or malformed
        if not message:
            raise ValueError("Empty request received")
        # Split the message and check if it has enough parts (e.g., method, path, version)
        message_parts = message.split()
        if len(message_parts) < 2:
            raise ValueError("Malformed HTTP request")
        
        filename=message_parts[1]  # Extract requested file name

        # Open and read the requested file
        f = open(filename[1:], 'r')  # Skip the leading "/" in the filename
        outputdata = f.read()
        f.close() 

        # Send HTTP header
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        #Send the content of the requested file to the client 
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

    except (IOError, ValueError) as e:
        #print(e)
        # Handle file not found (IOError) or malformed request (ValueError)
        try:#send http response and content
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode()) 
            connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())
        except BrokenPipeError: #this error occurs when connection closes or moves on at client level before server has actually sent data
            print("Broken pipe when sending 404 response to client")
    finally:
        # Ensure that the connection is closed even if there's an exception
        connectionSocket.close()

def webServer(port=6789):
    serverSocket = socket(AF_INET, SOCK_STREAM)  # Prepare a server socket
    serverSocket.bind(('', port))  # Bind server to port
    serverSocket.listen(1)  # maximum number of queued connections that the server will allow so server will listen to 1 client at a time
    print(f"Server is listening on port {port}...")

    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept()  # Accept the connection from the client
        print(f"Connection established for {addr}")
        # Start a new thread to handle the client request. so new thread for every request
        threading.Thread(target=handle_client, args=(connectionSocket,)).start()

if __name__ == "__main__": #as we're running the func as main program
    webServer(6789)
