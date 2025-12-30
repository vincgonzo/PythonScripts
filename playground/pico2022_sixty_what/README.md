🧨 Buffer Overflow CTF – 64‑bit (amd64) Practice

This challenge introduces stack‑based buffer overflows on 64‑bit Linux binaries, highlighting key differences from 32‑bit exploitation, especially canonical addresses and partial overwrites.

📌 Challenge Summary (64‑bit)

Architecture: amd64 (x86‑64)

Binary Type: ELF, dynamically linked

Protections:

NX enabled

No stack canary

No PIE (fixed addresses)

Goal: Redirect execution to a hidden flag() function

Vulnerability: Unsafe input (gets())

🔑 Key Differences from 32‑bit Exploitation
Topic	32‑bit (x86)	64‑bit (amd64)
Return address size	4 bytes	8 bytes
Stack alignment	loose	16‑byte aligned
Registers	EIP	RIP
Address space	small	canonical addresses
Overwrite style	full overwrite	often partial overwrite
📐 Stack Layout (64‑bit)

A typical vulnerable function looks like:

void vuln() {
    char buf[64];
    gets(buf);
}

Stack layout in memory:
| buffer (64 bytes) |
| saved RBP (8 bytes) |
| saved RIP (8 bytes) |  <-- control this


➡️ Offset to RIP = 64 + 8 = 72 bytes

🎯 Payload Structure (64‑bit)
Full overwrite (classic ret2win)
payload = b"A"*72 + p64(flag_addr)


Total payload size:

72 + 8 = 80 bytes

⚠️ Canonical Addresses (The Real Difficulty)

This is the core concept you were missing — and it’s subtle.

What is a canonical address?

On amd64, only the lower 48 bits of an address are used.

Valid user-space addresses look like:

0x00007fffffffffff


Invalid (non‑canonical) addresses crash immediately:

0x4141414141414141 ❌


The CPU requires that bits 48–63 are either:

all 0 (user space), or

all 1 (kernel space)

🧠 Why Partial Overwrites Work

Let’s say the saved return address on the stack is:

0x0000000000401236


In memory (little‑endian):

36 12 40 00 00 00 00 00


If you overwrite only the first 3 bytes:

3b 12 40


The address becomes:

0x000000000040123b


✅ Still canonical
✅ Upper bytes untouched
✅ Control flow hijacked

This is why sending only 3 bytes works in sixty_what.

🔬 Why This Is Different from 32‑bit

In 32‑bit:

You must overwrite all 4 bytes

Partial overwrite is rarely useful

In 64‑bit:

High bytes are often 0x00

Partial overwrite avoids:

bad bytes

newline truncation

stack alignment issues

This is intentional modern exploitation technique, not a hack.

🧪 Debugging in GDB (64‑bit)
Find offset
payload = cyclic(200)


Crash → inspect RIP:

info registers rip


Then:

cyclic_find(rip_value)


➡️ returns 72