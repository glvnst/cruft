#!/usr/bin/python
"""
wikitext - download the raw wikitext source of the named wikipedia article(s)
"""
import argparse
import os
import sys
import re
import urllib2


WIKITEXT_URL_FMT = 'http://en.wikipedia.org/w/index.php?title={}&action=raw'
USER_AGENT = 'wikitext/0.x (+https://github.com/glvnst/wikitext)'
REDIRECT_REGEX = re.compile(r'^\#REDIRECT \[\[(.+?)\]\]$')
MAX_REDIRECTS = 3


class FileExists(Exception):
    """
    This exception is raised when an output file already exists and overwrite
    is not enabled
    """
    pass


def wikify_string(title_string):
    """
    Return a string with proper quoting / formatting for use in a wikipedia
    article title
    """
    # For now, just convert spaces to underscores, then urlencode it
    return urllib2.quote(title_string.replace(' ', '_'))


def filenameify_string(title_string):
    """
    Return a string with the proper formatting as a filename on disk
    """
    # For now, just tack on a .txt extension and remove nonalpha/space chars
    return "{}.txt".format(re.sub(r'[^\w\ ]', '', title_string))


def article_read(article_title, redirect_count=0):
    """
    Return the content at a wikipedia URL after following any wiki redirects
    * The redirect_count argument is used internally to track recursive calls
    """
    url_opener = urllib2.build_opener()
    url_opener.addheaders = [('User-agent', USER_AGENT)]
    url = WIKITEXT_URL_FMT.format(wikify_string(article_title))

    data = url_opener.open(url).read()

    # Check for wikipedia redirects
    redirect_match = REDIRECT_REGEX.match(data)
    if redirect_match and redirect_count <= MAX_REDIRECTS:
        redirect_target = redirect_match.group(1)
        print 'Redirecting to "{}"'.format(redirect_target)
        return article_read(redirect_target, redirect_count + 1)

    return data


def download_article(article_title, output_path=None, allow_overwrite=False):
    """
    Download the contents of the article to the specified file, while honoring
    these principles:
    * don't talk to wikipedia until we have a valid output filehandle
    * don't clobber an existing file if there is a failure
    """
    performing_overwrite = False

    if output_path is None:
        sys.stdout.write(article_read(article_title))
        return True

    if os.path.exists(output_path):
        if allow_overwrite:
            performing_overwrite = True
        else:
            raise FileExists('The output file "{}" already exists.')

    try:
        with open(output_path, 'a') as file_out:
            file_out.write(article_read(article_title))
    except urllib2.HTTPError:
        # Cleanup the file if the request failed.
        # BUT If the file already existed, we leave it alone. Because we
        # opened it with 'a' instead of 'w', it should be unaffected.
        if not performing_overwrite:
            os.unlink(output_path)
        raise

    return True


def main():
    """ function called for command-line execution """

    argp = argparse.ArgumentParser('wikitext', description=(
        'Retrieve the raw wikipedia markup text for articles based on the '
        'specified article titles. Results are written to filenames '
        'corresponding to the article title, or optionally to STDOUT'))
    argp.add_argument('title', nargs='+', help=(
        'The plaintext title(s) of the article to retrieve. '
        'E.G. "Abraham Lincoln"'))
    argp.add_argument('--overwrite', action="store_true", help=(
        'Allow existing files to be overwritten by downloaded articles'))
    argp.add_argument('--stdout', action="store_true", help=(
        'Write articles to the standard output instead of to files on disk'))
    args = argp.parse_args()

    for title in args.title:
        if args.stdout:
            output_filename = None
        else:
            output_filename = filenameify_string(title)

        try:
            download_article(title, output_filename, args.overwrite)
        except FileExists:
            print 'The file "{}" already exists'.format(output_filename)
        except urllib2.HTTPError, exception:
            print 'When processing "{}" we got "{}"'.format(title, exception)
        else:
            if output_filename is not None:
                print 'Output written to "{}"'.format(output_filename)


if __name__ == '__main__':
    main()
