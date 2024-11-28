#!/bin/python3

"""
    Commutative: A ⊕ B = B ⊕ A
    Associative: A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
    Identity: A ⊕ 0 = A
    Self-Inverse: A ⊕ A = 0 
    
    KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313 
    KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
    KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
    FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf 
"""

from pwn import *
import base64


key1 = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
combo12 = bytes.fromhex("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e")
combo23 = bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1")
comboflag123 = bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf")


# Xor operations
flag = xor(comboflag123, xor(combo23, xor(key1, combo12))) # this commutative eliminate key3
flag = xor(flag, combo12) # this one and two

print(flag.hex())
print(flag.decode())
