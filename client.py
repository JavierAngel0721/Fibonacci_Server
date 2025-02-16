import socket
import argparse
import sys

# Files for logging client interaction
OK_LOG_FILE = "client-ok.out"
ERROR_LOG_FILE = "client-error.out"
BUFFER_SIZE = 1024
DEF_PORT = 10005

def send_request(server_ip, server_port, n):
    try:
        # Set up the socket connection
        server_address = (server_ip, server_port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Print the connection message
            print(f"Connecting to {server_ip} on port {server_port}...")
            client_socket.connect(server_address)

            # Send the number to the server
            client_socket.send(str(n).encode("ASCII"))
            client_socket.shutdown(socket.SHUT_WR)

            # Receive the server's response
            response = client_socket.recv(BUFFER_SIZE).decode("ASCII")
            return response

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Fibonacci Client")
    parser.add_argument("server_ip", help="IP address of the server")
    parser.add_argument("number", help="The number to send to the server")
    parser.add_argument("-p", "--port", type=int, default=DEF_PORT, help="Port number (default 10005)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    server_ip = args.server_ip
    server_port = args.port
    n = args.number

    # Send request and receive response from server
    response = send_request(server_ip, server_port, n)

    # Log response to appropriate file
    if response.startswith("OK"):
        # Log the full response (e.g., "OK 3")
        with open(OK_LOG_FILE, 'a') as ok_file:
            ok_file.write(f"{response}\n")
        # Print the full response (e.g., "OK 3")
        print(response)
    else:
        # Log the error message (e.g., "ERROR a non-negative integer input is required")
        with open(ERROR_LOG_FILE, 'a') as error_file:
            error_file.write(f"{response}\n")
        # Print the full error message (e.g., "ERROR a non-negative integer input is required")
        print(response)
