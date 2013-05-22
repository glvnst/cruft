#!/usr/bin/python

from ntlist import NTList

points = NTList("frame", "x", "y", "z", "intensity")

points.insert([0, 1, 1, 1, 10])
points.insert([0, 10, 2, 3, 11])
points.insert([0, 100, 3, 5, 12])
points.insert([0, 1000, 4, 7, 13])

search = lambda point: ((10 < point.intensity) and
                        (10 < point.x < 1500) and
                        (2 < point.y < 7))

for point in points.select(search):
    print "{0.frame}: {0.x},{0.y},{0.z} @ {0.intensity}".format(point)

"""
Output:
0: 100,3,5 @ 12
0: 1000,4,7 @ 13
"""
