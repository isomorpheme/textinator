import click
from PIL import Image

from textinator.image import TextImage, ColourImage

_default_palette = '@%8#$VYx*=+:~-. '

_resample_methods = {
    'nearest': Image.NEAREST,
    'bilinear': Image.BILINEAR,
    'bicubic': Image.BICUBIC,
    'antialias': Image.ANTIALIAS
}


@click.group()
def textinator():
    pass


@textinator.command()
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
@click.option('--background/--foreground', default=False,
              help="Wether to colour the foreground or"
              "background of characters. Does nothing if --colour"
              "is not present")
def convert(image, out, width, height, correct, resample,
            palette, invert, colour, background):
    """
    Converts INPUT to a text representation.
    OUT is an optional file to save to.

    Supports most image filetypes by default,
    except for JPEG. For that you need to install libjpeg.
    \b For more info see:
    http://pillow.readthedocs.org/installation.html#external-libraries
    """
    original = Image.open(image)
    original = original.convert(mode='RGB')

    if invert:
        palette = palette[::-1]

    if not width and not height:
        width, _ = click.get_terminal_size()

    size = _calculate_size(original.size, (width, height))

    resized = original.resize(size, resample=_resample_methods[resample])

    if correct:
        corrected_size = (size[0], int(size[1] * 0.5))
        resized = resized.resize(corrected_size,
                                 resample=_resample_methods[resample])

    if colour:
        result = ColourImage(resized, palette)
    else:
        result = TextImage(resized, palette)

    click.echo(result.text)


@textinator.command()
@click.argument('file', type=click.File('rb'))
def view(file):
    pass


def _calculate_size(original, target):
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
