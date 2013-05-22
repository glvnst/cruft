#!/usr/bin/python
""" Test the NTList class on Radiohead's head's head, now with visuals """
import os

import ntlist
import matplotlib
import pylab
from mpl_toolkits import mplot3d 

def load_points(input_directory):
    """
    Return an ntlist file
    """
    filename_sort = lambda filename: int(filename.split('.')[0])

    for filename in sorted(os.listdir(input_directory), key=filename_sort):
        basename, extension = os.path.splitext(filename)
        if extension == ".csv":
            with open(os.path.join(input_directory, filename)) as inputfile:
                for line in inputfile:
                    x, y, z, intensity = line.strip().split(',')
                    yield [basename, x, y, z, intensity]


points = ntlist.NTList("frame", "x", "y", "z", "intensity",
                       types=[int, float, float, float, int])
points.insert_generator(load_points('radiohead_hoc/frames'))
search = lambda point: ((60 < point.intensity) and
                        (25 < point.x < 150) and
                        (50 < point.y < 220))

extract = [next(points.select(search)) for _ in range(3500)]

FIGURE = pylab.figure()
A3D = mplot3d.Axes3D(FIGURE)
A3D.scatter([point.x for point in extract],
            [point.y for point in extract],
            [point.z for point in extract],
            c=[point.intensity for point in extract],
            marker=',')
matplotlib.pyplot.show()


