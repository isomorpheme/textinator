#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from PIL import Image
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset

_default_palette = ' ░▒▓█'

_resample_methods = {
    'nearest': Image.NEAREST,
    'bilinear': Image.BILINEAR,
    'bicubic': Image.BICUBIC,
    'antialias': Image.ANTIALIAS
}


@click.command()
@click.argument('image', type=click.File('rb'))
@click.argument('out', type=click.File('wt'), default='-',
                required=False)
@click.option('-w', '--width', type=click.INT,
              help="Width of output. If height is not given, "
                   "the image will be proportionally scaled.")
@click.option('-h', '--height', type=click.INT,
              help="Height of output. If width is not given, "
                    "the image will be proportionally scaled. "
                    "If neither width nor height are given, "
                    "the current terminal width is used instead.")
@click.option('--correct/--no-correct', default=True,
              help="Wether to account for the proportions of "
                   "monospaced characters. On by default.")
@click.option('-r', '--resample', default='antialias',
              type=click.Choice(['nearest', 'bilinear',
                                 'bicubic', 'antialias']),
              help="Filter to use for resampling. Default is antialias.")
@click.option('-p', '--palette', default=_default_palette,
              help="A custom palette for rendering images, "
                   "from from dark to bright.")
@click.option('-i', '--invert', is_flag=True,
              help="Inverts the palette.")
@click.option('-c', '--colour', is_flag=True,
              help="Enables colour output. This does not disable "
                   "the normal character palette. Rather, the characters "
                   "get a foreground colour corresponding to "
                   "the colour in the original.")
@click.option('--debug', is_flag=True,
              help="Debug mode.")
def convert(image, out, width, height, correct,
            resample, palette, invert, colour, debug):
    """
    Converts INPUT to a text representation.
    OUT is an optional file to save to.

    Supports most image filetypes by default,
    except for JPEG. For that you need to install libjpeg.
    \b For more info see:
    http://pillow.readthedocs.org/installation.html#external-libraries
    """

    original = Image.open(image)

    if invert:
        palette = palette[::-1]

    if not width and not height:
        width, _ = click.get_terminal_size()

    size = calculate_size(original.size, (width, height))

    resized = original.resize(size, resample=_resample_methods[resample])

    if correct:
        corrected_size = (size[0], int(size[1] * 0.5))
        resized = resized.resize(corrected_size,
                                 resample=_resample_methods[resample])

    if colour:
        adjusted = resized.convert(mode='RGB')
    else:
        adjusted = resized.convert(mode='L')

    for line in build_lines(adjusted, palette, colour):
        click.echo(line)

    if debug:
        click.echo("Original size {}\nRequest size {}\nResult size {}"
                   .format(original.size, (width, height), resized.size))


def calculate_size(original, target):
    """
    Proportionally scales image sizes.

    :param tuple original: the original size
    :param tuple target: the desired size
    :returns: the result size
    :rtype: tuple
    """

    original_width, original_height = original
    target_width, target_height = target

    ratio = original_height / original_width

    if target_width and not target_height:
        size = (target_width, int(target_width * ratio))
    elif target_height and not target_width:
        size = (int(target_height / ratio), target_height)
    elif target_width and target_height:
        size = (target_width, target_height)

    return size


def build_lines(image, palette, colour):
    """
    Generator function that iterates over an image and converts it to a
    text representation.

    :param :py:class:PIL.Image image: input image
    :param palette: character palette, ordered from dark to bright
    :type palette: str or list
    """

    width, height = image.size

    bw = image.convert(mode='L')

    for y in range(height):
        line = str()

        for x in range(width):
            value = bw.getpixel((x, y))
            char = value_to_char(value, palette)

            if colour:
                pixel = image.getpixel((x, y))
                char = rgb256(*pixel) + char + str(reset)

            line += char

        yield line


def value_to_char(value, palette, value_range=(0, 256)):
    """
    Takes a grayscale value and maps it to a character in a palette

    :param int value: input colour value
    :param palette: character palette, ordered from dark to bright
    :type palette: str or list
    :param tuple value_range: minimum and maximum value
    :raises ValueError: if the input value does not fall within value_range
    """

    if value not in range(*value_range):
        raise ValueError("Input value not in expected range.")

    palette_range = (0, len(palette))
    mapped = int(_scale(value, value_range, palette_range))
    return palette[mapped]


def _scale(value, source, destination):
    """
    Linear map a value from a source to a destination range.

    :param int value: original value
    :param tuple source: source range
    :param tuple destination: destination range
    :rtype: float
    """

    return (
        ((value - source[0]) / (source[1]-source[0]))
        * (destination[1]-destination[0])
        + destination[0]
    )
