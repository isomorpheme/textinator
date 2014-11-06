Textinator
==========
Textinator is a command line program that converts images to a text representation. You can use any set of characters to convert an image into. Furthermore, colour support is also present for those of you who want to view cat pictures in their terminal.

Installation
============
If you're not on Windows and want to convert JPEG or TIFF files, you will **first** need to install some dependencies. In most cases, you just need to install `libjpeg-dev` and `libtiff-dev` from your package manager (e.g. `apt-get` or `brew`). See [the Pillow documentation page external libraries](http://pillow.readthedocs.org/installation.html#external-libraries) for more info.

In any case, run this command to install Textinator:
```
$ pip install git+https://github.com/ijks/textinator.git
```

Usage
=====
```
Usage: textinate [OPTIONS] IMAGE [OUT]

  Converts INPUT to a text representation. OUT determines the output stream
  (stdout by default).

  Supports most image filetypes by default, except for JPEG. For that you
  need to install libjpeg. For more info see:
  http://pillow.readthedocs.org/installation.html#external-libraries

Options:
  -w, --width INTEGER             Width of output. If height is not given, the
                                  image will be proportionally scaled.
  -h, --height INTEGER            Height of output. If width is not given, the
                                  image will be proportionally scaled. If
                                  neither width nor height are given, the
                                  current terminal width is used instead.
  --correct / --no-correct        Wether to account for the proportions of
                                  monospaced characters. On by default.
  -r, --resample [nearest|bilinear|bicubic|antialias]
                                  Filter to use for resampling. Default is
                                  antialias.
  -p, --palette TEXT              A custom palette for rendering images, from
                                  from dark to bright.
  -i, --invert                    Inverts the palette.
  -c, --colour [8|16|256]         Enables colour output. This does not disable
                                  the normal character palette. Rather, the
                                  characters get a foreground colour
                                  corresponding to the colour in the original.
  --debug                         Debug mode.
  --help                          Show this message and exit.
```

