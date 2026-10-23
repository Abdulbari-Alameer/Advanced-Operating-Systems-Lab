import socket
import threading
import time


class Client:
    def __init__(self, client_id, host='localhost', port=9999):
        self.client_id = client_id
        self.host = host
        self.port = port

    def send_request(self, message):
        """Send a request to the server and receive response"""
        try:
            # Create socket connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))

            print(f"[Client{self.client_id}] Connected to server")

            # Send message
            print(f"[Client{self.client_id}] Sending: '{message}'")
            client_socket.send(message.encode('utf-8'))

            # Receive response
            response = client_socket.recv(1024).decode('utf-8')
            print(f"[Client{self.client_id}] Received: '{response}'")

            # Close connection
            client_socket.close()

        except Exception as e:
            print(f"[Client{self.client_id}] Error: {e}")


def run_client(client_id, delay=0):
    """Function to run a client with optional delay"""
    time.sleep(delay)  # Stagger client requests
    client = Client(client_id)
    client.send_request("hello")


if __name__ == "__main__":
    print("Starting 5 clients to send requests to server...")
    print("-" * 60)

    # Create and start 5 client threads
    client_threads = []
    for i in range(1, 6):
        thread = threading.Thread(target=run_client, args=(i, i * 0.5))
        thread.start()
        client_threads.append(thread)

    # Wait for all clients to complete
    for thread in client_threads:
        thread.join()

    print("-" * 60)
    print("All clients completed their requests")