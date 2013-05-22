#!/usr/bin/python
""" Test the NTList class on Radiohead's head's head """
import os
import ntlist


points = ntlist.NTList("frame", "x", "y", "z", "intensity")

input_directory = "radiohead_hoc/frames"
for filename in os.listdir(input_directory):
    basename, extension = os.path.splitext(filename)
    if extension == ".csv":
        with open(os.path.join(input_directory, filename)) as inputfile:
            for line in inputfile:
                x, y, z, intensity = line.strip().split(',')
                points.insert([int(basename), float(x), float(y), float(z),
                               int(intensity)])

search = lambda point: ((60 < point.intensity) and
                        (25 < point.x < 150) and
                        (50 < point.y < 220))

for point in points.select(search):
    print "{0.frame}: {0.x},{0.y},{0.z} @ {0.intensity}".format(point)

"""
Output:
who knows?
"""
