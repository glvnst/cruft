# Cruft

This is an archive of old projects and repos.

## Retired Github Repos

There isn't much of value in these retired repos.

* [**MapStack**](MapStack) (formerly <https://github.com/glvnst/MapStack>) - Python module which implements a stack of dicts, vertical key search, whiteouts
* [**checksome**](checksome) (formerly <https://github.com/glvnst/checksome>) - tool for recording filesystem metadata and file checksum snapshots
* [**delete_above**](delete_above) (formerly <https://github.com/glvnst/delete_above>) - Inkscape plugin: delete the selected object(s) and any objects on top of them
* [**ntlist**](ntlist) (formerly <https://github.com/glvnst/ntlist>) - Python collection of named tuples
* [**shlibs**](shlibs) (formerly <https://github.com/glvnst/shlibs>) - python module recursively finds app library dependencies, optionally can make a chroot jail with this info
* [**tctransform**](tctransform) (formerly <https://github.com/glvnst/tctransform>) - Tail Call Transform - a python decorator that rewrites recursive tail calls into iterations
* [**time_management**](time_management) (formerly <https://github.com/glvnst/time_management>) - a command-line utility for converting TaskPaper todo lists into BusyCal events
* [**turtleartiste**](turtleartiste) (formerly <https://github.com/glvnst/turtleartiste>) - python turtle module experiment
* [**wikitext**](wikitext) (formerly <https://github.com/glvnst/wikitext>) - command-line tool to download the raw wikitext source of the named wikipedia article(s)
* [**wx**](wx) (formerly <https://github.com/glvnst/wx>) - yahoo-powered command-line weather, the underlying service no longer exists

### About subrepo_adder

[`subrepo_adder.sh`](subrepo_adder.sh) is a tool that I use when I retire other repos into this one. It's a shell script which lets me clone my old repos into subdirs of this working directory, then add their contents to *this* repo without losing the commit date information. The date information is important for my reference but it also gives people encountering this repo a better idea of how old/untouched some of this stuff is.

#### Usage

```
Usage: ./subrepo_adder.sh [-h|--help] subrepo [...]

This script is for adding the contents of subrepos to the current repo
while maintaining the GIT_AUTHOR_DATE and GIT_COMMITTER_DATE.

Example Steps:

$ git init # if you haven't done this already
$ git clone some_repo.git
$ git clone some_other_repo.git
$ git clone some_third_repo.git
$ ./subrepo_adder.sh some_repo some_other_repo some_third_repo
$ git remote add origin some_repo_url_for_this_container_repo.git
$ git push
```