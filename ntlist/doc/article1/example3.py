#!/usr/bin/python
""" Test the NTList class on Radiohead's head's head, with lazy loading! """
import os
import ntlist

def load_points(input_directory):
    """
    Return an ntlist file
    """
    for filename in os.listdir(input_directory):
        basename, extension = os.path.splitext(filename)
        if extension == ".csv":
            with open(os.path.join(input_directory, filename)) as inputfile:
                for line in inputfile:
                    x, y, z, intensity = line.strip().split(',')
                    yield [int(basename), float(x), float(y), float(z),
                           int(intensity)]


points = ntlist.NTList("frame", "x", "y", "z", "intensity")
points.insert_generator(load_points('radiohead_hoc/frames'))
search = lambda point: ((60 < point.intensity) and
                        (25 < point.x < 150) and
                        (50 < point.y < 220))

for point in points.select(search):
    print "{0.frame}: {0.x},{0.y},{0.z} @ {0.intensity}".format(point)

"""
Output:
...
1: 25.411692,179.43275,-111.42092 @ 62
1: 25.371733,182.449,-113.35993 @ 108
1: 25.487768,185.37956,-113.74146 @ 114
...
"""
