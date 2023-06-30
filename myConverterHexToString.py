#!/usr/bin/python
import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 myConverter.py <mode> <value> <opt>")
        print("Modes: -s (string to hexa), -h (hexa to string), option 0/1 for strings<->hexa display")
        return

    mode = sys.argv[1]
    value = sys.argv[2]
    without = sys.argv[3] if mode == "-s" and len(sys.argv) >= 3 else False

    if mode == "-s":
        hexa_str = string_to_hex(value, without)
        print("string is {} character long.".format(len(hexa_str)))
        print("Value for string is : ")
        print(hexa_str)
    elif mode == "-h":
        str_val = hex_to_string(value)
        print("Value for hexadecimal is: ")
        print(str_val)
    else:
        print("Invalid. Please choose -s (string to hexa) or -h (hexa to string)")


def string_to_hex(string, without):
    hexa_string = ""
    without = True if without == "1" else False
    for char in string:
        hex_value = hex(ord(char))[2:].zfill(2)  # Convert ASCII value to hexadecimal and zero-pad
        hexa_string += "\\\\x" + hex_value.zfill(2) if without else " " + hex_value.zfill(2)
    return hexa_string


def hex_to_string(hexadecimal):
    hex_values = [hexadecimal[i:i+2] for i in range(0, len(hexadecimal), 2)]
    hexa_string = ""
    for hex_val in hex_values:
        hexa_string += "\\\\x" + hex_val
    return hexa_string


if __name__ == '__main__':
    main()