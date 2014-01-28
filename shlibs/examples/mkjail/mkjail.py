#!/usr/bin/python
"""
Creates a jail that contains the specified programs and their deps
"""
import shlibs
import argparse
import os
import sys
import subprocess


def build_standard_heirarchy(name, additional_dirs):
    """ Create some standard directories as defined by the hier manpage """
    hier = ['', 'bin', 'dev', 'etc', 'sbin', 'tmp', 'usr', 'usr/bin',
            'usr/include', 'usr/lib', 'usr/libexec', 'usr/local', 'usr/sbin',
            'usr/share', 'var', 'var/db', 'var/log', 'var/run', 'var/tmp']

    hier.extend(additional_dirs)

    for path in hier:
        os.mkdir(os.path.sep.join([name, path]))

    return


def build_jail(name, programs, additional_dirs=None, use_hardlinks=False):
    """
    Create a "jail" directory appropriate for chroot, with copies of the
    specified programs and their dependencies
    """

    dirname = os.path.dirname
    normpath = os.path.normpath
    pjoin = os.path.sep.join

    subdirs = {}

    build_standard_heirarchy(name, additional_dirs)

    components = reduce(lambda a, b: set(a)|set(b),
                        [shlibs.all_libraries_used(p) for p in programs
                         if os.path.isfile(p)])

    for component_path in components:
        dest_dir = normpath(pjoin([name, dirname(component_path)]))
        if dest_dir not in subdirs:
            subprocess.check_call(['mkdir', '-p', '--', dest_dir])
            subdirs[dest_dir] = True
        if use_hardlinks:
            subprocess.check_call(['ln', '--', component_path, dest_dir])
        else:
            subprocess.check_call(['cp', '-p', '--', component_path, dest_dir])

    return


if __name__ == '__main__':
    ARGP = argparse.ArgumentParser(description=(
        'Create a "jail" directory appropriate for chroot, with copies of '
        'the specified programs and their dependencies'))
    ARGP.add_argument('jail_name', help='the name of the jail to create')
    ARGP.add_argument('jail_programs', nargs="+",
                      help='full path programs to import into the jail')
    ARGP.add_argument('-l', '--link', action="store_true",
                      help=('use hard links instead of copies. '
                            '!!!WARNING!!!: Changes made to hard-linked '
                            'files in a jail will also affect the '
                            '"original" (and probably important) files '
                            'outside the jail. Additionally, hard links '
                            'cannot span filesystems. DO NOT USE THIS '
                            'OPTION UNLESS YOU KNOW WHAT YOU ARE DOING!'))

    ARGS = ARGP.parse_args()
    ADDITIONAL_DIRS = []

    if sys.platform == 'darwin':
        print "Adding dyld on OS X, because we almost always need it."
        ARGS.jail_programs.append('/usr/lib/dyld')
        ADDITIONAL_DIRS.extend(['Users', 'Users/Shared', 'var/folders',
                                'Applications', 'Applications/Utilities'])
    else:
        ADDITIONAL_DIRS.extend(['home'])

    build_jail(ARGS.jail_name, ARGS.jail_programs,
               additional_dirs=ADDITIONAL_DIRS,
               use_hardlinks=ARGS.link)
