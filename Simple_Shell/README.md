
myshell – Simple Custom Shell
This project implements a lightweight command-line shell written in C.
The shell reads user commands, creates a new process, and executes the command through the system’s default shell.
It provides a clean and minimal implementation that demonstrates core operating-system concepts such as process creation and command execution.
Project Overview
The program runs an interactive shell that waits for user input.
Each command is processed, cleaned, and executed inside a child process using fork, while the parent process waits until execution is complete.
The shell continues running until the user exits using Ctrl + D.

How to Compile
gcc myshell.c -o myshell

How to Run
./myshell
Examples of supported commands:
date
who
pwd
ls

