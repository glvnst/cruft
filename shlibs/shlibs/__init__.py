#!/usr/bin/python
"""
Print the complete list of shared libraries used by the specified binary
file(s) including any child dependencies.
"""
import sys

if sys.platform == 'darwin':
    from .shlibs_darwin import libraries_used
elif sys.platform.startswith('linux'):
    from .shlibs_linux2 import libraries_used
else:
    raise EnvironmentError(
        "I don't have support for {}, yet.".format(sys.platform))


def memoize(function):
    """
    memoization where only the first argument matters
    """
    class FirstArgMemoize(object):
        """ memoization where only the first argument matters """
        cache = None

        def __init__(self):
            self.cache = dict()

        def __getitem__(self, *key):
            if key[0] not in self.cache:
                self.cache[key[0]] = function(*key)
            return self.cache[key[0]]

    return FirstArgMemoize().__getitem__


# some optimizations
libraries_used = memoize(libraries_used)
if 'rpath_entries' in locals():
    rpath_entries = memoize(rpath_entries)


def all_libraries_used(executable_path):
    """
    Return a list of the paths of the shared libraries used by the object file
    (or executable) at the specified executable_path AND ALL SHARED LIBRARIES
    WHICH THEY USE
    """
    visited = dict()

    def reentrant_resolve(path, parent_deps=None):
        """ This sub-function is re-entered to perform the nested lookups """
        result = [path]
        visited[path] = True

        if parent_deps is None:
            parent_deps = list()

        dependencies = libraries_used(path, parent_deps)
        if dependencies is not None:
            for dep in dependencies:
                if dep not in visited:
                    result.extend(reentrant_resolve(dep,
                                                    parent_deps + [path,]))
        return result

    return set(reentrant_resolve(executable_path))
