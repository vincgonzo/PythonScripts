#!/bin/python3


import time


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'Exec time: {end - start} sec')
    return wrapper

def greating(func):
    def wrapper(*args, **kwargs):
        print('Hello,')
        func(*args, **kwargs)
    return wrapper

#@greating
@measure_time
def morning(name):
    print(f'Good morning, {name}')


morning('John')
