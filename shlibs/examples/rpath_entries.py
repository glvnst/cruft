#!/usr/bin/python
""" Print the rpath entries from the Mach-O headers of the specified files """
import argparse
from shlibs import shlibs_darwin


def main():
    """ The primary function for commandline execution """
    argp = argparse.ArgumentParser(description=(
        "Print the rpath entries from the Mach-O headers of the specified "
        "file(s)"))
    argp.add_argument('file', nargs="+", help=(
        "The file(s) to print the rpath entries from"))
    args = argp.parse_args()

    for file_path in args.file:
        print "{}:".format(file_path)
        for entry in shlibs_darwin.rpath_entries(file_path):
            print "  {!r}".format(entry)

if __name__ == '__main__':
    main()
