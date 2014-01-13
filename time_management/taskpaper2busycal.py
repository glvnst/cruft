#!/usr/bin/python
"""
Import the todo items from a taskpaper file into busycal
"""
import argparse
import urllib
import subprocess
import re


TODO_REGEX = re.compile(r'^\s*-\s+(.+?)(?:\s@.+)?\s*$')


def todos_from_file(input_file):
    """
    Read the specified input file and return a list of todo items
    (without the leading "-" and without any @tags)
    """
    result = list()
    with open(input_file, 'r') as input_file:
        for line in input_file:
            matched = TODO_REGEX.match(line)
            if matched:
                result.append(matched.group(1))
    return result


def busycal_todo_url(todo_string, target_calendar):
    """
    return a busycal todo URL from the specified string and target_calendar
    """
    return "busycalevent://new/-{}%20%2F{}".format(
        urllib.quote(todo_string, ''), urllib.quote(target_calendar))


def open_url(url):
    """
    open the specified URL using the native OS X 'open' command
    """
    subprocess.check_call(['open', url])


def main(files, target_calendar):
    """ Read the specified files, open the corresponding BusyCal URLS """
    for input_file in files:
        for todo in todos_from_file(input_file):
            open_url(busycal_todo_url(todo, target_calendar))


if __name__ == "__main__":
    ARGP = argparse.ArgumentParser(
        description='Import taskpaper todo items into busycal')
    ARGP.add_argument('file', nargs="+",
                      help='the path to the taskpaper file(s) to import')
    ARGP.add_argument('-c', '--calendar', default="Personal",
                      help=('the name of the calendar in which the todo '
                            'items should be created (default: Personal)'))
    ARGS = ARGP.parse_args()

    main(ARGS.file, ARGS.calendar)
