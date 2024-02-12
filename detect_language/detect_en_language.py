#!/bin/python


ALPHA = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
EN_WORDS = []

def get_data():
    dictionary = open("en_words.txt", "r")
    for w in dictionary.read().split('\n'):
        EN_WORDS.append(w)
    dictionary.close()

def count_words(txt):
    txt = txt.upper()
    words = txt.split(" ")
    #print(words)
    matches = 0
    while("" in words):
        words.remove("")
    for word in words:
        if word in EN_WORDS:
            #print("result for this word %s find in dictionary", word)
            matches = matches + 1
    return matches

def is_txt_english(txt):
    matches = count_words(txt)
    if(float(matches) / len(txt.split('\n'))) * 100 >= 90:
        return True
    return False

def caesar_crack(cipher_txt):
    for key in range(len(ALPHA)):
        plain_txt = ''
        for c in cipher_txt:
            idx = ALPHA.find(c)
            idx = (idx-key)%len(ALPHA)
            plain_txt = plain_txt + ALPHA[idx]
        if is_txt_english(plain_txt):
            print("We have managed to crack Caesar cipher, the key is: %s, the message is : %s" % (key, plain_txt))

if __name__ == "__main__":
    get_data()
    encrypted = "VJKUBKUBCBOGUUCIG"
    caesar_crack(encrypted)
