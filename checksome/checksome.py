#!/usr/bin/env python
"""
checksome: collect and compare checksums and stats for files on disk
"""
import argparse
import sys
import os
import stat
import hashlib

#import support_modules

STAT_FIELDS = sorted([attr for attr in dir(os.lstat('/'))
                      if attr.startswith("st_")])


def get_file_info(file_path):
    """ Return the stats and sha1 hash of the given file """
    # get the stats
    try:
        file_stats = os.lstat(file_path)
    except OSError:
        # this usually means permission to stat the file is denied
        file_stats = os.stat_result(['oserr']*len(STAT_FIELDS))

    # get the hash (if the file is a regular file)
    if file_stats.st_mode is not 'oserr' and stat.S_ISREG(file_stats.st_mode):
        # if it is a regular file, get the checksum
        try:
            with open(file_path) as handle:
                file_hash = hashlib.sha1(handle.read()).hexdigest()
        except IOError:
            file_hash = "ioerr"
    else:
        file_hash = "na"

    return (file_stats, file_hash)


def scan_directory(target, output_handle):
    """
    walk the given target path and print the results to the given output
    filehandle
    """
    target_path = os.path.abspath(target)
    target_stats = os.lstat(target_path)
    target_device = target_stats.st_dev

    # write the header
    output_handle.write('#checksome 1\n')
    output_handle.write("#" + ",".join(['path', 'hash'] + STAT_FIELDS) + "\n")

    # walk the target directory
    for (directory, subdirs, files) in os.walk(target_path):
        for filename in files:
            file_path = os.path.join(directory, filename)
            (file_stats, file_hash) = get_file_info(file_path)

            # write the file info
            output_handle.write(",".join([file_path, file_hash] +
                                         [str(getattr(file_stats, attr))
                                          for attr in STAT_FIELDS]) +
                                "\n")

        # prune subdirectories on different devices
        # this prevents os.walk from visiting them in subsequent iterations
        for subdir in subdirs:
            subdir_fullpath = os.path.join(directory, subdir)
            subdir_stats = os.lstat(subdir_fullpath)
            if subdir_stats.st_dev != target_device:
                subdirs.remove(subdir)
                sys.stderr.write("pruning {}\n".format(subdir_fullpath))


def main():
    """
    primary function for command-line execution. return an exit status integer
    or a bool type (where True indicates successful exection)
    """
    argp = argparse.ArgumentParser(description=(
        "collect and compare checksums and stats for files on disk"))
    argp.add_argument('target', nargs="+", help=(
        "directory to scan"))
    argp.add_argument('-d', '--debug', action="store_true", help=(
        "enable debugging output"))
    args = argp.parse_args()

    # do things
    for target in args.target:
        scan_directory(target, sys.stdout)

    return True


if __name__ == '__main__':
    try:
        RESULT = main()
    except KeyboardInterrupt:
        sys.stderr.write("\n\nExiting on keyboard command\n")
        RESULT = False
    sys.exit(int(not RESULT if isinstance(RESULT, bool) else RESULT))
