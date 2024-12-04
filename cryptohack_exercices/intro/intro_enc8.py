#!/bin/python3

"""
For the next few challenges, you'll use what you've just learned to solve some more XOR puzzles.
I've hidden some data using XOR with a single byte, but that byte is a secret. Don't forget to decode from hex first.
"""

from binascii import unhexlify
from pwn import *
import base64
"""
# Function to XOR the hex string with a single byte key
def xor_hex_string(hex_string, key):
    # Convert the hex string to bytes
    byte_data = bytes.fromhex(hex_string)
    # XOR each byte with the key
    return bytes([byte ^ key for byte in byte_data])

def starts_with_crypto(data):
    # Check if the first 6 characters are "crypto" (case-sensitive)
    return data[:6] == b"crypto"

# Function to check if the output contains readable ASCII characters
def is_printable(data):
    # Check if all characters in data are printable (ASCII)
    return all(32 <= byte <= 126 for byte in data)

# Function to brute force the XOR key
def brute_force_xor(hex_string):
    # Try all keys from 0x00 to 0xFF
    for key in range(256):
        # XOR the hex string with the current key
        decrypted_data = xor_hex_string(hex_string, key)
        
        # Convert the result to a string (assuming it's ASCII)
        decoded_str = decrypted_data.decode('ascii', errors='ignore')
        
        if starts_with_crypto(decrypted_data):
            print(f"Key: 0x{key:02X} - Decrypted text: {decoded_str}")

def brute_force_xor_with_possible_keys(hex_string, possible_keys):
    for key_string in possible_keys:
        print(f"Key: {key_string} - start the test")
        # Ensure the key string is a single byte (as XOR works with single bytes)
        if len(key_string) >= 1:
            key = key_string.encode()  # Convert the key string to its byte value
            
            # XOR the hex string with the current key
            decrypted_data = xor(hex_string, key)
            
            # Convert the result to a string (assuming it's ASCII)
            decoded_str = decrypted_data.decode()

            # Check if the decrypted data starts with "crypto"
            print(f"Key: '{key_string}' - Decrypted text: {decoded_str}")

# Example usage
if __name__ == "__main__":
    # The hex string to brute force
    hex_string = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"  # Example: "Hello, World" in hex

    possible_keys = ['myXORkeymyXORkeymyXORkeymyXORkeymyXORkeymy', 'crypto{}', 'crypto{FLAG}', 'signature']  # Example list of possible keys
    
    # Start brute forcing with the given possible keys
    brute_force_xor_with_possible_keys(hex_string, possible_keys)
   """


def brute(input, key):
    if len(input) != len(key):
        return "Failed!"

    output = b''
    for b1, b2 in zip(input, key):
        output += bytes([b1 ^ b2])
    try:
        return output.decode("utf-8")
    except:
        return "Cannot Decode some bytes"

data = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
cipher = unhexlify(data)
print("[-] CIPHER: {}".format(cipher))

# First Step
key_part = brute(cipher[:7], "crypto{".encode())
print("[-] PARTIAL KEY FOUND: {}".format(key_part)) 

# Second Step
key = (key_part + "y").encode()
key += key * int((len(cipher) - len(key))/len(key))
key += key[:((len(cipher) - len(key))%len(key))]
print("[-] Decoding using KEY: {}".format(key))

plain = brute(cipher, key)
print("\n[*] FLAG: {}".format(plain))
