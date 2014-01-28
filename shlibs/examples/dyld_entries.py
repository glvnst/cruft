#!/usr/bin/python
""" Print the dyld entries from the Mach-O headers of the specified files """
import argparse
from shlibs import shlibs_darwin


def main():
    """ The primary function for commandline execution """
    argp = argparse.ArgumentParser(description=(
        "Print the dyld entries from the Mach-O headers of the specified "
        "file(s)"))
    argp.add_argument('file', nargs="+", help=(
        "The file(s) to print the dyld entries from"))
    args = argp.parse_args()

    for file_path in args.file:
        print "{}:".format(file_path)
        for ref in shlibs_darwin.shared_libraries(file_path):
            tag = "weak-ref:" if ref.is_weak else ""
            print "  {}{}".format(tag, ref.path)


if __name__ == '__main__':
    main()
