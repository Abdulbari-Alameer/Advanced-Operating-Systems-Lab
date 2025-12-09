# Multithreaded Client-Server Framework

A Python implementation of a concurrent client–server architecture using a **thread pool** design pattern.  
This project demonstrates efficient handling of multiple client connections using a pre-created pool of worker threads.

---

## 📌 Verify Python Installation

```bash
python3 --version
Usage
1. Start the Server
python3 server.py

2. Run the Clients

Open another terminal:

python3 client.py


Run it multiple times to simulate multiple clients.

3. Stop the Server

Press:

Ctrl + C


You will see:

[SERVER] Shutting down...
[SERVER] Server stopped

🔍 How It Works
🖥️ Server Side
Initialization

Creates 5 worker threads (Thread1 → Thread5)

Each worker waits on a thread-safe queue for incoming tasks

Request Processing

Main thread accepts client connections

Each connection is pushed into the task queue

Next available worker thread picks up the task

Worker processes the message and sends a response

Thread Assignment

Requests are processed by first available thread

Different clients may be handled by different threads

Response contains the thread ID (e.g., Thread3)

👤 Client Side
Connection

5 clients run concurrently

Each client runs in its own thread

Communication

Connects to localhost:9999

Sends: "hello"

Receives response:
"Hi, responding with Thread{N}"

Closes connection after receiving response
