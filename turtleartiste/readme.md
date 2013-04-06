# Turtle Artiste

## Quick Note

This is a terrible name. We must fix it, you and I.

## Overview

This python script leverages the native python turtle module. We have an easy algorithm. We generate a number of output .ps files. We then convert those to various other formats.

Weird things are done, for example:

* .ps -> .png(s) -> .html -> [a giant aggregated].png
* .ps -> .png -> .gif(s) -> [an animated].gif

## Requirements

I'm sorry. It starts strong, then gets *stupid*.

* python 2.x with the native [turtle module][] (and the native tk stuff to make it work)
* Make
* ghostscript (with the png16m output device, should be standard)
* [Caractères L1][], the font (or change turtle_artiste.py to use a font that you have)
* the `convert` executable from imagemagick (`brew install imagemagick`)
* gifsicle (`brew install gifsicle`)
* webkit2png (`brew install webkit2png`) 

## To Do

1. Virtually every part of this could be faster. Some of the discrete steps like png > gif could be sped up by running a few processes in parallel. Probably also, I could do the big combination in postscript and then render it out that way.

2. Use a python [steganography library][] to embed offensive `fortune -o` output in individual images. Fun!

3. Get a reason for making this thing / spending any more time on it.


[turtle module]: http://docs.python.org/2/library/turtle.html
[Caractères L1]: http://en.wikipedia.org/wiki/Caract%C3%A8res
[steganography library]: http://domnit.org/stepic/doc/