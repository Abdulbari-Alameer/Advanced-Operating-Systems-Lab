
# RPC WHO Program – Local & Remote User Info Service

This project provides:
- A local WHO tool that reads active login sessions from `/var/run/utmp`.
- A remote WHO system using ONC RPC, where a client requests login information from a remote server.

---

## Project Structure
Advanced-Operating-Systems-Lab/
│── src/ # All C source files (local_who + RPC)
│── docs/ # readme

---

## Part A — Local WHO

**File:** `src/local_who.c`  
Reads UTMP records using `setutent()`, `getutent()`, and `endutent()`.

**Compile**
```bash
gcc -Wall src/local_who.c -o local_who
Run
./local_who
________________________________________
Part B — RPC WHO
Includes:
remote.x
remote_server.c
remote_client.c
remote_clnt.c
remote_svc.c
remote_xdr.c
________________________________________
Install dependencies (Ubuntu 22.04+)
sudo apt-get update
sudo apt-get install -y build-essential libtirpc-dev rpcbind rpcsvc-proto
________________________________________
Generate RPC files
rpcgen remote.x
________________________________________
RPC Implementation
1. Create RPC interface (remote.x)
•	Define the RPC program and structure.
•	Run:
•	rpcgen remote.x
•	This generates:
o	remote.h
o	remote_clnt.c
o	remote_svc.c
o	remote_xdr.c
________________________________________
2. Implement the Server
•	Create remote_server.c
•	Implement the function:
•	user_info *get_users_1()
________________________________________
3. Implement the Client
•	Create remote_client.c
•	Create RPC handle:
•	clnt = clnt_create(host, REMOTE_PROG, REMOTE_VERS, "tcp");
•	Call:
•	GET_USERS_1(NULL, clnt);
________________________________________
4. Compile (Ubuntu 22.04 uses libtirpc)
gcc -Wall -o remote_server remote_server.c remote_svc.c remote_xdr.c -ltirpc
gcc -Wall -o remote_client remote_client.c remote_clnt.c remote_xdr.c -ltirpc
________________________________________
5. Start rpcbind
sudo systemctl start rpcbind
________________________________________
6. Run the programs
Terminal 1 (server):
./remote_server
Terminal 2 (client):
./remote_client localhost

-
.

