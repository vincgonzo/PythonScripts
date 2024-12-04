#!/bin/python
from binascii import unhexlify

flag_s = '63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d'

# first way
flag_bytes = bytes.fromhex(flag_s)
print(flag_bytes);

# method with unhexlify
flag_decode = unhexlify(flag_s)
print(flag_decode);
