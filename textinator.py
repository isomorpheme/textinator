import click
from PIL import Image

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
@click.option('-p', '--palette', default='█▓▒░ ',
              help="A custom palette for rendering images. Goes from dark to bright.")
@click.option('-w', '--width', type=click.INT,
              help="Width of output. If height is not given, the image will be proportionally scaled.")
@click.option('-h', '--height', type=click.INT,
              help="Height of output. If width is not given, the image will be proportionally scaled.")
@click.option('--correct/--no-correct', default=True,
              help="Wether to account for the proportions of monospaced characters. On by default.")
@click.option('-r', '--resample', default='antialias',
              type=click.Choice(['nearest', 'bilinear', 'bicubic', 'antialias']),
              help="Filter to use for resampling. Default is antialias.")
@click.option('--debug', is_flag=True,
              help="Debug mode.")
def convert(image, out, width, height, palette,
            resample, correct, debug):
    """
    Converts an input image to a text representation.
    Writes to stdout by default. Optionally takes another file as a second output.

    Supports most filetypes, except JPEG.
    For that you need to install libjpeg.
    For more info see:\n
    http://pillow.readthedocs.org/installation.html#external-libraries
    """

    original = Image.open(image)
    if debug: original.show()

    original_width, original_height = original.size
    ratio = min(original_height / original_width,
                original_width / original_height)

    if not width and not height:
        width, _ = click.get_terminal_size()
        size = (width, int(width * ratio))
    elif width and not height:
        size = (width, int(width * ratio))
    elif height and not width:
        size = (int(height / ratio), height)
    elif width and height:
        size = (width, height)

    resized = original.resize(size, resample=_resample_methods[resample])

    if debug: resized.show()

    if correct:
        corrected_size = (size[0], int(size[1] * 0.5))
        resized = resized.resize(corrected_size, resample=_resample_methods[resample])
        if debug: resized.show()

    bw = resized.convert(mode="L")

    if debug: bw.show()

    for line in build_lines(bw, palette):
        click.echo(line)

    if debug: click.echo("Original size {} (ratio {})\nRequest size {}\nResult size {}".format(
                         original.size, ratio, (width, height), resized.size))


def build_lines(image, palette):
    width, height = image.size

    for y in range(height):
        line = ''

        for x in range(width):
            pixel = image.getpixel((x, y))
            line += value_to_char(pixel, palette)

        yield line


def value_to_char(value, palette, value_range=(0, 256)):
    palette_range = (0, len(palette))
    mapped = int(scale(value, value_range, palette_range))
    return palette[mapped]


def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]
