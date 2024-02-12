#!/bin/python


ALPHABET = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def vigenere_encrypt(plain_txt, key):
    plain_txt = plain_txt.upper()
    key = key.upper()

    cipher_txt = ''
    key_index = 0

    for character in plain_txt:
        idx = (ALPHABET.find(character)+(ALPHABET.find(key[key_index]))) % len(ALPHABET)
        cipher_txt = cipher_txt + ALPHABET[idx]

        key_index = key_index + 1
        if key_index == len(key):
            key_index = 0
    return cipher_txt

def vigenere_decrypt(cipher_txt, key):
    cipher_txt = cipher_txt.upper()
    key = key.upper()

    plain_txt = ''
    key_index = 0

    for character in cipher_txt:
        idx = (ALPHABET.find(character)-(ALPHABET.find(key[key_index]))) % len(ALPHABET)
        plain_txt = plain_txt + ALPHABET[idx]

        key_index = key_index + 1
        if key_index == len(key):
            key_index = 0
    return plain_txt 

if __name__ == "__main__":
    plain_txt = "The other approach to concealing plaintext structure in the ciphertext involves using several different monoalphabetic substitution ciphers rather than just one; the key specifies which particular substitution is to be employed for encrypting each plaintext symbol. The resulting ciphers, known generically as polyalphabetics, have a long history of usage. The systems differ mainly in the way in which the key is used to choose among the collection of monoalphabetic substitution rules."
    encrypted = vigenere_encrypt(plain_txt, 'secret')
    print('Encrypted message: %s\n' % encrypted)
    decrypted = vigenere_decrypt(encrypted, 'secret')
    print('Decrypted message: %s\n' % decrypted)
