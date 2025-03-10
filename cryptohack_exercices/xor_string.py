#!/bin/python

import argparse
import binascii

def xor_encrypt_decrypt(input_string: str, key_pattern: str) -> str:
    # Extend the key pattern to match the length of the input string
    extended_key = (key_pattern * (len(input_string) // len(key_pattern))) + key_pattern[:len(input_string) % len(key_pattern)]
    
    # Show the repeated key pattern
    print(f"Repeated Key Pattern (extended to match input length): {extended_key}")
    
    # XOR each character in the input string with the corresponding character in the extended key
    result = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(input_string, extended_key))
    
    # Show the XOR result in a hex format to visualize non-printable characters
    hex_result = binascii.hexlify(result.encode('utf-8')).decode('utf-8')
    print(f"XOR Result (Hex): {hex_result}")
    
    return result

def main():
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a string using a repeating XOR key.")
    
    # Add arguments for encryption and decryption operations
    parser.add_argument("-e", "--encrypt", help="Encrypt the string", action="store_true")
    parser.add_argument("-d", "--decrypt", help="Decrypt the string", action="store_true")
    
    # Add arguments for the string and key pattern
    parser.add_argument("input_string", help="The string to encrypt or decrypt")
    parser.add_argument("key_pattern", help="The key pattern to repeat for XOR")
    
    # Parse the arguments
    args = parser.parse_args()

    # Check if both encrypt and decrypt flags are not set
    if args.encrypt == args.decrypt:
        print("Error: You must specify either -e (encrypt) or -d (decrypt).")
        parser.print_help()
        return
    
    # Get the operation type and execute accordingly
    if args.encrypt:
        print(f"Encrypting the string: {args.input_string}")
        encrypted = xor_encrypt_decrypt(args.input_string, args.key_pattern)
        print(f"Encrypted string (UTF-8): {encrypted}")
    
    elif args.decrypt:
        print(f"Decrypting the string: {args.input_string}")
        decrypted = xor_encrypt_decrypt(args.input_string, args.key_pattern)
        print(f"Decrypted string (UTF-8): {decrypted}")

if __name__ == "__main__":
    main()

