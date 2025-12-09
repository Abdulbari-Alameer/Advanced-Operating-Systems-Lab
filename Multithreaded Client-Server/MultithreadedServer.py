import socket
import threading
from queue import Queue
import time


class ThreadPoolServer:
    def __init__(self, host='localhost', port=9999, num_workers=5):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.task_queue = Queue()
        self.workers = []
        self.server_socket = None
        self.running = False

    def worker_thread(self, worker_id):
        """Worker thread that processes client requests"""
        print(f"[SERVER] Thread{worker_id} started and ready")

        while self.running:
            try:
                # Get client connection from queue (timeout to check running flag)
                client_socket, client_addr = self.task_queue.get(timeout=1)

                print(f"[Thread{worker_id}] Handling client {client_addr}")

                # Receive data from client
                data = client_socket.recv(1024).decode('utf-8')
                print(f"[Thread{worker_id}] Received: '{data}' from {client_addr}")

                # Process request and send response
                if data.lower() == 'hello':
                    response = f"Hi, responding with Thread{worker_id}"
                    client_socket.send(response.encode('utf-8'))
                    print(f"[Thread{worker_id}] Sent: '{response}' to {client_addr}")
                else:
                    response = f"Thread{worker_id} received: {data}"
                    client_socket.send(response.encode('utf-8'))

                # Close client connection
                client_socket.close()
                self.task_queue.task_done()

            except:
                # Queue.get() timeout is normal - just continue waiting
                continue

    def start(self):
        """Start the server and worker threads"""
        self.running = True

        # Create worker threads
        for i in range(1, self.num_workers + 1):
            worker = threading.Thread(target=self.worker_thread, args=(i,))
            worker.daemon = True
            worker.start()
            self.workers.append(worker)

        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)

        print(f"[SERVER] Listening on {self.host}:{self.port}")
        print(f"[SERVER] Worker pool size: {self.num_workers}")
        print("-" * 60)

        try:
            while self.running:
                # Accept client connection
                client_socket, client_addr = self.server_socket.accept()
                print(f"[SERVER] New connection from {client_addr}")

                # Add to task queue for worker threads
                self.task_queue.put((client_socket, client_addr))

        except KeyboardInterrupt:
            print("\n[SERVER] Shutting down...")
        finally:
            self.stop()

    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("[SERVER] Server stopped")


if __name__ == "__main__":
    server = ThreadPoolServer(host='localhost', port=9999, num_workers=5)
    server.start()