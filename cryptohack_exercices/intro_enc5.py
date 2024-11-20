#!/bin/python3

from pwn import *
import base64


ciphertxt = "label"
cipher_bytes = ciphertxt.encode()
key = 13
key_encode = bytes([key])

print(cipher_bytes)
print(key_encode)

# Xor operation
xored_str = xor(cipher_bytes, key_encode)

print(f"crypto{{{xored_str}}}")
