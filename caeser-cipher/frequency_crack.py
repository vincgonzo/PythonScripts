#!/bin/python
import matplotlib.pylab as plt


LETTERS = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def freq_ana(plain_txt):
    plain_txt = plain_txt.upper()
    letter_frequency = {}
    for l in  LETTERS:
        letter_frequency[l] = 0

    for letter in plain_txt:
        if letter in  LETTERS:
            letter_frequency[letter] += 1
    return letter_frequency

def plot_distribution(letter_freq):
    centers = range(len(LETTERS))
    plt.bar(centers, letter_freq.values(), align='center', tick_label=letter_freq.keys())
    plt.xlim([0, len(LETTERS)-1])
    plt.show()

def caeser_crack(cipher_txt):
    letter_freq = freq_ana(cipher_txt)
    print(letter_freq)
    plot_distribution(letter_freq)

if __name__ == "__main__":
    cipher_txt = "PMGOLGOHKGHUE OPUNGJVUMPKLU PHSG VGZHEGOLGCYV LGP GPUGJPWOLYG OH GPZGIEGZVGJOHUNPUNG OLGVYKLYGVMG OLGSL  LYZGVMG OLGHSWOHIL G OH GUV GHGCVYKGJVASKGILGTHKLGVA ."
    caeser_crack(cipher_txt)
