#!/bin/python3

from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from settings import KEY, KEY_LEN_REQ
import string, random

def pad_for_key(key):
    while len(key) % KEY_LEN_REQ != 0:
        # random_letter = random.choice(string.ascii_uppercase) v2 to implement
        key += "P"
    return key

# Fernet package generator
# key = Fernet.generate_key()
cipher = Fernet(urlsafe_b64encode(pad_for_key(KEY).encode()))
# token = cipher.encrypt(b"My super secret I don't want to be disclosed.")
# print(type(token))
# print(f"token : {token}")
# result = cipher.decrypt(token)
# print(type(result))
# print(f"In clear text : {result}")