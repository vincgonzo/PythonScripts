#!/bin/python


ALPHABET = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KZY = 3



def caeser_encrypt(plain_txt):
    cipher_txt = ''
    plain_txt = plain_txt.upper()

    for c in plain_txt:
        index = ALPHABET.find(c)
        index = (index+KZY) %len(ALPHABET)
        cipher_txt = cipher_txt + ALPHABET[index]

    return cipher_txt


def caeser_decrypt(cipher_txt):
    plain_txt = ''

    for c in cipher_txt:
        index = ALPHABET.find(c)
        index = (index-KZY) % len(ALPHABET)
        plain_txt = plain_txt + ALPHABET[index]
    return plain_txt


if __name__ == "__main__":
    encrypted = caeser_encrypt('This is an example')
    print(encrypted)
    decrypted = caeser_decrypt(encrypted)
    print(decrypted)

