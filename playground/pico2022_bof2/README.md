🧨 Buffer Overflow CTF – Practice Challenge

Welcome to this introductory binary exploitation (pwn) challenge 🎯
This project is designed for local, educational practice to understand classic stack-based buffer overflows on 32-bit Linux binaries.

📌 Challenge Summary

Architecture: x86 (32-bit)

Binary Type: ELF, dynamically linked

Protections: Intentionally weakened for learning

Goal: Trigger the hidden win() function to print the flag

The program reads user input using an unsafe function, making it vulnerable to a stack buffer overflow.

📂 Project Structure
.
├── vuln.c        # Vulnerable source code
├── Makefile      # Build configuration
├── vuln          # Compiled binary (after build)
└── flag.txt      # Flag file (create locally)

🛠️ Requirements

Linux (recommended)

gcc with 32-bit support

make

gdb (recommended for debugging)

Install dependencies on Debian/Ubuntu:

sudo apt update
sudo apt install gcc-multilib gdb make

⚙️ Build Instructions

Compile the binary using:

make


This will produce a vulnerable 32-bit binary named vuln.

To clean the directory:

make clean

🚩 Creating the Flag

The program expects a file called flag.txt in the same directory.

Create one for local testing:

echo "CTF{local_test_flag}" > flag.txt


🧪 Debugging with GDB

Debugging is highly encouraged for this challenge.

Start GDB:

gdb ./vuln

There a payload.py script written with pwntool that give the complete method and answer to finish but it is highly encourage
to first test / understand before using it.