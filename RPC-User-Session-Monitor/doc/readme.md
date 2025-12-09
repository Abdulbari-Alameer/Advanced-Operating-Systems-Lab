# RPC Who Command Implementation

A distributed system implementation that displays logged-in users using Remote Procedure Call (RPC) in C. This project demonstrates client-server communication using Sun RPC protocol on Linux.

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## 🎯 Overview

This project implements the Unix `who` command functionality in two ways:

1. **Part A (Local)**: Reads the `/var/run/utmp` database directly to display currently logged-in users
2. **Part B (RPC)**: Uses Remote Procedure Call (RPC) to fetch user information from a remote server

The project showcases distributed computing concepts, inter-process communication, and system programming in C.

## ✨ Features

- **Local User Monitoring**: Direct access to system utmp database
- **Remote User Monitoring**: RPC-based distributed architecture
- **Real-time Information**: Displays current logged-in users with:
  - Username
  - Terminal (TTY)
  - Login time
  - Remote host (if applicable)
- **Cross-platform Support**: Works on Ubuntu 22.04 LTS and compatible Linux distributions
- **Lightweight**: Minimal dependencies and resource usage

## 🏗️ System Architecture

```
┌─────────────┐                    ┌─────────────┐
│   Client    │                    │   Server    │
│             │                    │             │
│  Remote     │  ─── RPC Call ──>  │   Remote    │
│  Client     │                    │   Server    │
│             │  <── Response ───  │             │
│             │                    │ (reads utmp)│
└─────────────┘                    └─────────────┘
                                          │
                                          ▼
                                   ┌─────────────┐
                                   │ /var/run/   │
                                   │    utmp     │
                                   └─────────────┘
```

## 📋 Prerequisites

### System Requirements
- **OS**: Ubuntu 22.04 LTS or compatible Linux distribution
- **RAM**: Minimum 512MB
- **Disk Space**: 100MB free space
- **Processor**: Any modern x86/x64 processor

### Software Requirements
- GCC Compiler (version 7.0 or higher)
- GNU Make
- RPC libraries (libtirpc-dev)
- rpcbind service
- rpcsvc-proto

### Verify Prerequisites

```bash
# Check Ubuntu version
lsb_release -a

# Check GCC
gcc --version

# Check if rpcgen is available
which rpcgen
```

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/rpc-who-command.git
cd rpc-who-command
```

### Step 2: Install Dependencies

```bash
# Update package list
sudo apt-get update

# Install required packages
sudo apt-get install -y build-essential libtirpc-dev rpcbind rpcsvc-proto
```

Or use the automated setup script:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Step 3: Compile the Programs

```bash
# Make compile script executable
chmod +x scripts/compile.sh

# Run compilation
./scripts/compile.sh
```

Or compile manually:

```bash
# Compile local who command
gcc -Wall src/local/local_who.c -o local_who

# Generate RPC files
cd src/rpc && rpcgen remote.x && cd ../..

# Compile RPC server
gcc -Wall -I/usr/include/tirpc -o remote_server \
    src/rpc/remote_server.c \
    src/rpc/remote_svc.c \
    src/rpc/remote_xdr.c \
    -ltirpc

# Compile RPC client
gcc -Wall -I/usr/include/tirpc -o remote_client \
    src/rpc/remote_client.c \
    src/rpc/remote_clnt.c \
    src/rpc/remote_xdr.c \
    -ltirpc
```

### Step 4: Start rpcbind Service

```bash
# Start the service
sudo systemctl start rpcbind

# Enable on boot
sudo systemctl enable rpcbind

# Verify it's running
sudo systemctl status rpcbind
```

## 💻 Usage

### Part A: Local Who Command

Display locally logged-in users:

```bash
./local_who
```

**Sample Output:**
```
===========================================
Local WHO Command - Part A
===========================================

Reading from: /var/run/utmp

USER         TTY          LOGIN TIME           HOST            
================================================================
john         pts/0        2024-12-09 14:30     192.168.1.100
alice        pts/1        2024-12-09 15:45     -

Total users logged in: 2
```

### Part B: RPC Implementation

#### Terminal 1 - Start the Server

```bash
./remote_server
```

The server will start and wait for client connections.

#### Terminal 2 - Run the Client

```bash
# Connect to localhost
./remote_client localhost

# Or connect to a remote server
./remote_client 192.168.1.50
```

**Sample Output:**
```
===========================================
RPC Client - Part B
===========================================

Attempting to connect to RPC server at localhost...
✓ Connected successfully!

Calling remote procedure GET_USERS...

===========================================
Remote Server Response:
===========================================

USER         TTY          LOGIN TIME           HOST            
================================================================
john         pts/0        2024-12-09 14:30     192.168.1.100
alice        pts/1        2024-12-09 15:45     -

Total users: 2

===========================================
✓ Connection closed.
```

### Testing with Multiple Users

```bash
# Open multiple SSH sessions or terminals
# Then run the client to see all active users

./remote_client localhost
```

## 📁 Project Structure

```
rpc-who-command/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
│
├── src/                     # Source code
│   ├── local/              # Local implementation
│   │   └── local_who.c     # Local who command
│   └── rpc/                # RPC implementation
│       ├── remote.x        # RPC interface definition
│       ├── remote_server.c # RPC server implementation
│       └── remote_client.c # RPC client implementation
│
├── docs/                    # Documentation
│   ├── INSTALLATION.md     # Detailed installation guide
│   └── USAGE.md           # Detailed usage instructions
│
├── scripts/                # Build and setup scripts
│   ├── compile.sh         # Compilation script
│   └── setup.sh          # Environment setup script
│
└── examples/              # Sample outputs and demos
    └── sample_output.txt  # Example program outputs
```

## 🔧 Technical Details

### Technologies Used

- **Language**: C (C99 standard)
- **RPC Protocol**: Sun RPC (ONC RPC)
- **Libraries**: 
  - libtirpc (Transport Independent RPC)
  - utmp.h (User accounting database)
  - time.h (Time formatting)
- **Build Tools**: GCC, rpcgen

### How It Works

#### Part A: Local Implementation
1. Opens `/var/run/utmp` database using `setutent()`
2. Iterates through entries using `getutent()`
3. Filters `USER_PROCESS` type entries
4. Formats and displays user information
5. Closes database using `endutent()`

#### Part B: RPC Implementation

**Server Side:**
1. Defines RPC interface in `remote.x`
2. Generates stub code using `rpcgen`
3. Implements `get_users_1_svc()` function
4. Registers with portmapper (rpcbind)
5. Waits for client requests

**Client Side:**
1. Creates RPC client handle using `clnt_create()`
2. Calls remote procedure `get_users_1()`
3. Receives and displays results
4. Destroys client handle

### RPC Interface Definition

```c
program REMOTE_PROG {
    version REMOTE_VERS {
        user_info GET_USERS(void) = 1;
    } = 1;
} = 0x20000001;
```

- **Program Number**: 0x20000001
- **Version Number**: 1
- **Procedure Number**: 1 (GET_USERS)

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. "Cannot find utmp file" Error

**Solution:**
```bash
# Check if file exists
ls -la /var/run/utmp

# If not, create it
sudo touch /var/run/utmp
```

#### 2. "rpcbind not running" Error

**Solution:**
```bash
# Start rpcbind
sudo systemctl start rpcbind
sudo systemctl enable rpcbind

# Check status
sudo systemctl status rpcbind
```

#### 3. "Connection refused" Error

**Solution:**
```bash
# Check if server is running
ps aux | grep remote_server

# Check RPC services
rpcinfo -p localhost

# Restart server
./remote_server
```

#### 4. Compilation Errors

**Solution:**
```bash
# Reinstall dependencies
sudo apt-get install --reinstall libtirpc-dev

# Clean and rebuild
rm -f remote_server remote_client local_who
rm -f src/rpc/remote.h src/rpc/remote_*.c
./scripts/compile.sh
```

#### 5. No Users Showing (WSL/Virtual Environment)

This is normal in WSL or some virtual environments. The utmp database may be empty. Try:

```bash
# Compare with system commands
who
w
users

# These may also show nothing, which is expected
```

### Getting Help

If you encounter issues:

1. Check the [INSTALLATION.md](docs/INSTALLATION.md) guide
2. Review [USAGE.md](docs/USAGE.md) for correct usage
3. Search existing GitHub issues
4. Create a new issue with:
   - Your OS version
   - Error messages
   - Steps to reproduce

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards

- Follow Linux kernel coding style
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License - Copyright (c) 2024 [Your Name]
```

## 👤 Author

**Your Name**

- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: your.email@example.com
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- **Course**: Operating Systems / Distributed Systems
- **Institution**: Your University Name
- **Instructor**: Professor Name
- **References**: 
  - Stevens & Rago - "Advanced Programming in the UNIX Environment"
  - Sun Microsystems RPC Documentation
  - Linux Manual Pages

## 📊 Project Status

![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📚 Additional Resources

- [RPC Tutorial](https://docs.oracle.com/cd/E19683-01/816-1435/rpcintro-46812/index.html)
- [utmp Manual Page](https://man7.org/linux/man-pages/man5/utmp.5.html)
- [libtirpc Documentation](https://sourceforge.net/projects/libtirpc/)

## 🔗 Related Projects

- [rpcgen Examples](https://github.com/topics/rpcgen)
- [Distributed Systems in C](https://github.com/topics/distributed-systems)

---

**⭐ If you find this project helpful, please give it a star!**

**📫 Questions? Open an issue or reach out!**

---

*Last Updated: December 2024*
