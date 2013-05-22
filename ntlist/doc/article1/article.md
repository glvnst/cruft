# A Python Module For Storage of Tables

I've been thinking about the interface for a python module designed to contain a table/matrix, composed of rows and columns, a bit like a sql table. I considered an implementation based on a list of lists for the primary storage and a dict that maps column offsets to a string-based accessor. But instead I've been working with a list of namedtuples. This seems to do the job very nicely. Here's a simple example of the interface for this "named-tuple list" module ("`ntlist`"):

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

Obviously this is an overly simple example case. The essential idea is to efficiently store a large list of things which are "efficiently" accesible by a name that is determined during runtime. Here's an example with a much larger dataset: the 2008 [Radiohead "House of Cards" LIDAR data](http://code.google.com/p/radiohead/).

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


This code tries to load everything into memory. That is more than 25 million records, containing more than 51 million integers and more than 76 million floating-point numbers all loaded into memory at one time. That's more than 960 GB of raw variable data (assuming 64-bit underlying implementations). This simply won't work with the 4GB hardware I'm working on. So I need to make a change! To that end, I added the option to only load the data as it is needed:

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

The insert_generator function replaces the NTList instance's internal row storage list with the given generator, so that generator-compatible iterators and enumerators can load data when needed, and dispose of it when it is no-longer needed. Now the script stays a manageable size in memory during its entire exection.

One thing that I wondered about was the type conversion taking place on the final line of the `load_points` function. Is this the best place? Does is make my generator more or less portable? What if there are other data sources? I decided to move type conversion into the ntlist class. The constructor now takes an optional `types` argument which specifies a list of types (which correspond to the given list of column names). If column type is specified, values inserted into it are automatically type-converted.

But what would such a class look like in action? For that I'll use [matplotlib](http://matplotlib.org):

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

Examples of output:

![Radiohead - House of Cards LIDAR - ntlist example 1](http://media.tumblr.com/f29e21d07a4a1cbbb6cef47623be0a55/tumblr_inline_mn6tjpki4p1qz4rgp.jpg)

![Radiohead - House of Cards LIDAR - ntlist example 2](http://media.tumblr.com/9975a53c97137470697b28b304858bb0/tumblr_inline_mn6tktJb4S1qz4rgp.jpg)

![Radiohead - House of Cards LIDAR - ntlist example 3](http://media.tumblr.com/4052366036981e1aba96127ad4156688/tumblr_inline_mn6tm2we9w1qz4rgp.jpg)
    
The missing step is benchmarking. I'll save that for next time. In the mean time, the [ntlist module is on github](https://github.com/glvnst/ntlist).