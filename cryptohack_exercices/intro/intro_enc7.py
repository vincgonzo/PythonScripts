#!/bin/python3

"""
For the next few challenges, you'll use what you've just learned to solve some more XOR puzzles.
I've hidden some data using XOR with a single byte, but that byte is a secret. Don't forget to decode from hex first.
"""
from binascii import unhexlify
import string
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

# first brut force method
ciphertext = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")
find_xor_key_and_decode(ciphertext)
print("/!\ --- second method start here --- /!\ ")

def single_byte_xor(input, key):
    if len(chr(key)) != 1:
      raise "KEY LENGTH EXCEPTION: In single_byte_xor key must be 1 byte long!"

    output = b''
    for b in input:
        output += bytes([b ^ key])

    try:
        return output.decode("utf-8")
    except:
        return "Cannot Decode some bytes"

data = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
decoded = unhexlify(data)

print("[-] HEX_DECODE: {}\n".format(decoded))

result = {}
for i in range(256):
    result[i] = (single_byte_xor(decoded, i))
    #print("[-] KEY: {}\nSTRING: {}".format(i,single_byte_xor(decoded, i)))

print("[*] FLAG: {}".format([s for s in result.values() if "crypto" in s]))
