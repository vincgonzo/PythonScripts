#!/bin/python

ALPHA = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def caeser_crack(cipher_txt):
    for k in range(len(ALPHA)):
        plain_txt = ''
        for c in cipher_txt:
            idx = ALPHA.find(c)
            idx = (idx-k)%len(ALPHA)
            plain_txt = plain_txt + ALPHA[idx]
        print('With key %s, the result is : %s'%(k, plain_txt))



if __name__ == "__main__":
    encrypted = 'VJKUBKUBCBOGUUCIG'
    caeser_crack(encrypted)
