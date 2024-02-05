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

if __name__ == "__main__":
    plain_txt = "Shanon defiend the quantity of infos produced by here source"

    frequencies = freq_ana(plain_txt)
    plot_distribution(frequencies)
