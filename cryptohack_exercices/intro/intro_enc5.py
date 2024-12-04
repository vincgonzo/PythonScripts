#!/bin/python3

from pwn import *
import base64

# first method pwntool
ciphertxt = "label"
cipher_bytes = ciphertxt.encode()
key = 13
key_encode = bytes([key])

print(cipher_bytes)
print(key_encode)

# Xor operation
xored_str = xor(cipher_bytes, key_encode)
print("=== RESULT with pwnTool ======")
print(f"crypto{{{xored_str}}}")

# second only python
flag = ''

for c in ciphertxt:
    flag += chr(ord(c) ^ key)

print("=== RESULT with python ======")
print('crypto{{{}}}'.format(flag))
