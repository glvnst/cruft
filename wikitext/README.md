# wikitext

A small command-line program that downloads the raw wikipedia markup text for the specified article. It does not download images or other supporting media. It does not follow links.

It is designed as a shortcut to using `curl` or `wget` in situations where you want article **markup**. For example, to get the raw markup for the "Abraham Lincoln" article, you'd normally run `wget 'http://en.wikipedia.org/w/index.php?title=Abraham_Lincoln&action=raw'`; with wikitext, you can instead run `wikitext "Abraham Lincoln"`

**This program is not a robot, it is not optimized for large numbers of downloads. Don't abuse wikipedia.**

## Examples

Specify the plaintext article title.

	% wikitext "Stochastic optimization"
	Output written to "Stochastic optimization.txt"

You can specify multiple titles. Why not use your shell's builtin globbing?:

	%  wikitext {Haskell,Erlang}" (programming language)"
	Output written to "Haskell programming language.txt"
	Output written to "Erlang programming language.txt"

Automagic wiki redirects are supported:

	% ./wikitext.py 'wikitext'
	Redirecting to "Wiki markup"
	Output written to "wikitext.txt"

## Help Message


	usage: wikitext [-h] [--overwrite] [--stdout] title [title ...]
	
	Retrieve the raw wikipedia markup text for articles based on the specified
	article titles. Results are written to filenames corresponding to the article
	title, or optionally to STDOUT
	
	positional arguments:
	  title        The plaintext title(s) of the article to retrieve. E.G.
	               "Abraham Lincoln"
	
	optional arguments:
	  -h, --help   show this help message and exit
	  --overwrite  Allow existing files to be overwritten by downloaded articles
	  --stdout     Write articles to the standard output instead of to files on
	               disk

## License

The program license is BSD-like. For details, see LICENSE.txt
