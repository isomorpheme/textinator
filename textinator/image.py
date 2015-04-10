class TextImage():
    def __init__(self, original, palette):
        self.original = original
        self.palette = palette
        self.lines = self._build_lines()
        self.text = self._build_text()

    def _build_text(self):
        result = str()

        for line in self.lines:
            result += line + '\n'

        return result

    def _build_lines(self):
        result = list()
        width, height = self.original.size

        for y in range(height):
            line = str()

            for x in range(width):
                value = self.original.getpixel((x, y))
                char = self._value_to_char(value)
                line += char

            result.append(line)

        return result

    def _value_to_char(self, value):
        if type(value) is int or len(value) != 3:
            raise TypeError("Value should be a 3-tuple")

        r, g, b = value
        luminosity = 0.2 * r + 0.72 * g + 0.07 * b

        palette_range = (0, len(self.palette))
        mapped = int(_scale(luminosity, (0, 256), palette_range))
        char = self.palette[mapped]

        return char


class ColourImage(TextImage):
    def __init__(self, *args, background=False):
        self.background = background
        super().__init__(*args)

    def _value_to_char(self, value):
        from ansi.colour.rgb import rgb256
        from ansi.colour.fx import reset

        char = super()._value_to_char(value)
        colour = rgb256(*value)
        if self.background:
            colour.replace('38', '48', 1)
            # Modify the ANSI escape code to use bg instead of fg

        return colour + char + str(reset)


class Animation():
    def __init__(frames, speed):
        pass


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
