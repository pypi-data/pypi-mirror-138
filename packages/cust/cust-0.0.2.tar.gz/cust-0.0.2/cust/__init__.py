# COPYRIGHT - mi66mc

'''
    Custom library and utils.
    Copyright - mi66mc
'''

import os

class math_:

    def calc(x):
        # "x" to string, "y"
        y = str(x)
        # return "y"
        return eval(y)

    def to_comma(x):
        y = str(x)
        return y.replace('.', ',')

    def percentage(x : int, y : int):
        z = x * y / 100
        return z
    
    def square_root(x : float):
        return float(x) ** 0.5

class utils:

    def clean():
        os.system('cls' if os.name == 'nt' else 'clear')

def info():
    print("Custom library and utils.\nCopyright - mi66mc\n\nSimple library with utils.")