RPC WHO Program – Local & Remote User Info Service
This project provides:
•	A local WHO tool that reads active login sessions from /var/run/utmp.
•	A remote WHO system using ONC RPC, where a client requests login information from a remote server.

🔹** Project Structure**
Advanced-Operating-Systems-Lab/
│── src/        # All C source files (local_who + RPC)
│── docs/       # Reports (optional)
│── images/     # Screenshots
└── README.md

**Part A Local WHO**
File: src/local_who.c
Reads UTMP records using setutent(), getutent(), and endutent().
Compile
gcc -Wall src/local_who.c -o local_who
Run
./local_who

**Part B  RPC WHO**
Includes:
remote.x
remote_server.c
remote_client.c
remote_clnt.c
remote_svc.c
remote_xdr.c
Install dependencies (Ubuntu 22.04+)
sudo apt-get update
sudo apt-get install -y build-essential libtirpc-dev rpcbind rpcsvc-proto
Generate RPC files
rpcgen remote.x
Compile
gcc -Wall -I/usr/include/tirpc -o remote_server remote_server.c remote_svc.c remote_xdr.c -ltirpc
gcc -Wall -I/usr/include/tirpc -o remote_client remote_client.c remote_clnt.c remote_xdr.c -ltirpc
Run
Server:
./remote_server
Client:
./remote_client localhost

