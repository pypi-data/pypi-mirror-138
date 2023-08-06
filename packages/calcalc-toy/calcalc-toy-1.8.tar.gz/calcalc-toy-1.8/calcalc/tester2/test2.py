from calcalc.CalCalc import calculate


"""
This file tests relative imports.
"""


def printer2():
    print('This is printer2 in package tester2, module test2.py!')


if __name__ == "__main__":
    print('1 + 1 = ' + str(calculate('1+1', local=False)))
