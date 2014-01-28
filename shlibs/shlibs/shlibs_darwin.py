#!/usr/bin/python
"""
Print the complete list of shared libraries used by the specified binary
file(s) including any child dependencies.
"""
import platform
import os
import sys
from macholib import MachO, mach_o
from collections import namedtuple

ShlibRef = namedtuple('ShlibRef', ['path', 'is_weak'])
CURRENT_SYSTEM = [platform.processor(), platform.machine()]

class NotFoundError(Exception):
    """ Raised when a shared library can't be found """
    pass


def warn(string):
    """
    Print a warning to stderr
    """
    sys.stderr.write("{}\n".format(string))


def is_current_architecture(header):
    """
    Return True if the given header matches the current machine's architecture
    """
    if MachO.CPU_TYPE_NAMES[header.cputype] in CURRENT_SYSTEM:
        return True

    return 


def libraries_used(binary_file, parent_deps=None):
    """
    Return a list of fully resolved shared library paths used by the given
    binary_file
    """

    if parent_deps is None:
        parent_deps = list()
    exists = os.path.exists
    result = list()

    for ref in shared_libraries(binary_file):
        try:
            if ref.path.startswith('@'):
                resolved_path = expand_load_variables(ref.path, binary_file,
                                                      parent_deps)
            else:
                resolved_path = ref.path

            if not exists(resolved_path):
                raise NotFoundError("Not found: {}, referenced by {}".format(
                    resolved_path, binary_file))
        except NotFoundError:
            if not ref.is_weak:
                raise
            # Weak references don't need to exist
        else:
            result.append(resolved_path)

    return result


def shared_libraries(binary_file):
    """
    Return a list of the shared libraries referenced by a Mach-O binary
    """
    result = list()

    try:
        headers = MachO.MachO(binary_file).headers
    except ValueError:
        warn("skipping {}, it is probably not a Mach-O file".format(
            binary_file))
        return []
    except IOError:
        warn("skipping {}, it is probably not a regular file".format(
            binary_file))
        return []

    for architecture_header in headers:
        if is_current_architecture(architecture_header.header):
            result.extend([ShlibRef(load_path, 'weak' in load_type)
                           for _, load_type, load_path
                           in architecture_header.walkRelocatables()])
        else:
            warn("skipping header in {} with arch {}".format(binary_file,
                MachO.CPU_TYPE_NAMES[architecture_header.header.cputype]))

    return result


def rpath_entries(binary_file):
    """
    Return a list of rpath entries in the specified binary file

    The mach-O header should list contain a list of rpaths to be tried when
    attempting to process the actual load commands in the rest of the header

    This could easily be a list comprehension, but this is a bit more readable

    The original version was inspired by rpath.list_rpaths @:
    https://github.com/enthought/machotools/tree/master/machotools
    """
    result = list()

    for architecture_header in MachO.MachO(binary_file).headers:
        for _, command, data in architecture_header.commands:
            if type(command) is not mach_o.rpath_command:
                continue
            # the entry is null terminated, so we take that out.
            entry = data.rstrip(b'\x00')
            if entry.startswith('@loader_path'):
                # it is important to expand loader_path now because it refers
                # to the path of the file that contains the @loader_path entry
                entry = expand_load_variables(entry, binary_file)
            result.append(entry)

    return result


def resolve_rpath(rpath_spec, binary_file, parent_deps=None):
    """
    Return a resolved filesystem path for a given rpath-based library path 

    This code is mostly copied from rpath.list_rpaths @:
    https://github.com/enthought/machotools/tree/master/machotools
    """
    if parent_deps is None:
        parent_deps = list()
    # Some shortcuts for speed and readability
    normpath = os.path.normpath
    exists = os.path.exists

    run_path_list = reduce(lambda a, b: a + b,
                           [rpath_entries(path) for path
                            in parent_deps + [binary_file]])

    if False:
        print ("resolve_rpath:\n"
               "  rpath_spec: {}\n"
               "  binary_file: {}\n"
               "  parent_deps: {!r}\n"
               "  run_path_list: {!r}\n\n").format(rpath_spec, binary_file,
               parent_deps, run_path_list)

    for entry in run_path_list:
        if entry.startswith('@'):
            entry = expand_load_variables(entry, binary_file, parent_deps)

        test_path = normpath(rpath_spec.replace("@rpath", entry, 1))

        if exists(test_path):
            return test_path

    # If we're still here, no vaild rpath expansion was found.
    raise NotFoundError(("Couldn't resolve {} reference in {} using entries "
        "{} and binary_file={}").format(rpath_spec, binary_file,
        run_path_list, os.path.dirname(binary_file)))


def expand_load_variables(path_spec, binary_file, parent_deps=None):
    """ Replace the Mach-O load variables with actual values """

    if parent_deps is None or len(parent_deps) == 0:
        parent_deps = [binary_file,]

    # Some shortcuts for speed and readability
    normpath = os.path.normpath
    dirname = os.path.dirname

    result = path_spec
    if path_spec.startswith("@executable_path"):
        executable_path = parent_deps[0]
        result = normpath(path_spec.replace("@executable_path",
                                            dirname(executable_path), 1))
    elif path_spec.startswith("@loader_path"):
        result = normpath(path_spec.replace("@loader_path",
                                            dirname(binary_file), 1))
    elif path_spec.startswith("@rpath"):
        result = resolve_rpath(path_spec, binary_file, parent_deps)

    return result

