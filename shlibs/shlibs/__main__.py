#!/usr/bin/python
""" The handler for direct module call """
import argparse
from . import libraries_used, all_libraries_used


def main():
    """ The primary function executed for command-line execution """
    argp = argparse.ArgumentParser(prog='-mshlibs', description=('Print the '
        'complete list of shared libraries used by the specified binary '
        'file(s), (optionally including all child dependencies)'))
    argp.add_argument('file', nargs='+', help='file(s) to report on')
    argp.add_argument('-a', '--all', action="store_true", help=(
        "recursively resolve all sub-dependencies"))
    args = argp.parse_args()

    if args.all:
        deps = reduce(lambda a, b: a|b,
                      [all_libraries_used(f) for f in args.file])
    else:
        deps = reduce(lambda a, b: set(a)|set(b),
                      [libraries_used(f) for f in args.file])

    for path in sorted(deps):
        print path

if __name__ == '__main__':
    main()
