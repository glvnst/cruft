#!/usr/bin/python
""" Test for tctransform decorator """
from tctransform import tct
import timeit

def add(a, b):
    """ Silly Peano addition example code """
    if a == 0:
        return b
    return add(a-1, b+1)

if __name__ == "__main__":
    print "recursive", timeit.timeit("add(200, 1)",
                                     setup="from __main__ import add")
    add = tct(add)
    print "iterative", timeit.timeit("add(200, 1)",
                                     setup="from __main__ import add")
