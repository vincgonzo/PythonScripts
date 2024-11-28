#!/bin/python3

"""
For the next few challenges, you'll use what you've just learned to solve some more XOR puzzles.
I've hidden some data using XOR with a single byte, but that byte is a secret. Don't forget to decode from hex first.
"""

from pwn import *
import base64

def xor_decrypt(ciphertext, key):
    return bytes([b ^ key for b in ciphertext])

def is_valid_utf8(decoded_bytes):
    try:
        decoded_bytes.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

def find_xor_key_and_decode(ciphertext):
    # Try all possible keys (0-255)
    for key in range(256):
        decrypted = xor_decrypt(ciphertext, key)
        
        if is_valid_utf8(decrypted):
            decoded_string = decrypted.decode()
            # Check if the string starts with "crypto{"
            if decoded_string.lower().startswith("crypto"):
                print(f"Key: {key} - Decoded string: {decoded_string}")

    print("-- Finished and check all keys")

ciphertext = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")
find_xor_key_and_decode(ciphertext)
