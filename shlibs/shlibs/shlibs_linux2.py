#!/usr/bin/python
"""
Print the complete list of shared libraries used by the specified binary
file(s) including any child dependencies.
"""
import subprocess
import re
#import pdb

LDD_STYLE1 = re.compile(r'^\t(.+?)\s\=\>\s(.+?)?\s\(0x.+?\)$')
LDD_STYLE2 = re.compile(r'^\t(.+?)\s\(0x.+?\)$')

def libraries_used(binary_path, _):
    """
    Return a list of the paths of the shared libraries used by the object file
    (or executable) at the specified binary_path
    """
    try:
        raw_output = subprocess.check_output(['ldd', '--', binary_path],
                                             stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, exception:
        if 'not a dynamic executable' in exception.output:
            return None
        else:
            raise

    # We can expect output like this:
    # [tab]path1[space][paren]0xaddr[paren]
    # or
    # [tab]path1[space+]=>[space+]path2?[paren]0xaddr[paren]
    # path1 can be ignored if => appears
    # path2 could be empty

    if 'statically linked' in raw_output:
        return None

    result = []
    for line in raw_output.splitlines():
        match = LDD_STYLE1.match(line)
        if match is not None:
            if match.group(2):
                result.append(match.group(2))
            continue

        match = LDD_STYLE2.match(line)
        if match is not None:
            result.append(match.group(1))
            continue

        print "warning: unrecognized ldd output line: '{}'".format(line)

    return result if result else None

