from PIL import Image
from os import get_terminal_size

default_palette = list('░▒▓█')

print(get_terminal_size())

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


def value_to_char(value, palette=default_palette, value_range=(0, 256)):
    palette_range = (0, len(palette))
    mapped = int(scale(value, value_range, palette_range))
    return palette[mapped]


def convert_image(image_path):
    original = Image.open(image_path)
    width, height = original.size

    thumb = original.copy()
    thumb.thumbnail(get_terminal_size())

    bw = thumb.convert(mode="L")
    width, height = bw.size

    for y in range(height):
        line = ''
        for x in range(width):
            line += value_to_char(bw.getpixel((x, y)))
        print(line)

    bw.show()

if __name__ == '__main__':
    convert_image('doge.jpg')