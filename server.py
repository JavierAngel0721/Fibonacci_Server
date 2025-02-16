import logging
import socket
import argparse

LOG_FILE = "server.out"
BUFFER_SIZE = 1024
DEF_PORT = 10005 

# Set up logging to the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def handle_request(data):
    try:
        # parse the number
        n = int(data.strip())  #Strip the extra spaces
        if n < 0:
            return "ERROR a non-negative integer input is required"
        else:
            return f"OK {fib(n)}"
    except ValueError:
        return "ERROR a non-negative integer input is required"

def start_server(port=DEF_PORT):
    try:
        # Create a server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(1)

        logging.info(f"Server started, listening on port {port}...")

        while True:
            peer_socket, peer_address = server_socket.accept()
            logging.info(f"Accepted connection from {peer_address}")

            with peer_socket:
                # Receive data from the client
                data = peer_socket.recv(BUFFER_SIZE).decode("ASCII")
                logging.info(f"Received data: {data}")
                response = handle_request(data)
                logging.info(f"Sending response: {response}")
                peer_socket.send(response.encode("ASCII"))

            logging.info(f"Disconnected from {peer_address}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Fibonacci Server")
    parser.add_argument("-p", "--port", type=int, default=DEF_PORT, help="Port number (default 10005)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    start_server(port=args.port)
