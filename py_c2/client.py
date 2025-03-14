#!/bin/python3


import requests

x = requests.get('http://localhost')
print(x.text)
