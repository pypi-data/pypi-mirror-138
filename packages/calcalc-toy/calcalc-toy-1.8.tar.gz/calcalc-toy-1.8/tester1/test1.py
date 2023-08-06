from calcalc.CalCalc import calculate
from calcalc.tester2 import test2


"""
This file tests relative imports.
"""


def printer1():
    print('This is printer1 in package tester1, module test1.py!')


if __name__ == "__main__":
    print('1 + 1 = ' + str(calculate('1+1', local=False)))
    test2.printer2()
