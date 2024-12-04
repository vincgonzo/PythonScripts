#!/bin/python3

from binascii import unhexlify
import base64


cipher = '72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf';
hex = unhexlify(cipher) # or bytes.fromhex(cipher)

print(base64.b64encode(hex));
