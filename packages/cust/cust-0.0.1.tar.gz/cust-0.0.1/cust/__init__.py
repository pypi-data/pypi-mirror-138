# COPYRIGHT - mi66mc

'''
    Custom library and utils.
    Copyright - mi66mc
'''

import os

def calc(x):
    # "x" to string, "y"
    y = str(x)
    # return "y"
    return eval(y)

def clean():
    os.system('cls' if os.name == 'nt' else 'clear')

def verify(x):
    if x in globals():
        return True
    else:
        return False

def to_comma(x):
    y = str(x)
    return y.replace('.', ',')

def info():
    print("Simple library with utils.")