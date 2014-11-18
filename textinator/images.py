class Image():
    def __init__(self, original, palette):
        self.original = original
        self.palette = palette

        self.lines = self._build_lines()

    def _build_lines(self):
        pass

    def _value_to_char(self, value, value_range=(0, 256)):
        pass


class ColourImage(Image):
    def _value_to_char(self, *args, **kwargs):
        char = super()._value_to_char(*args, **kwargs)
        colour = 'colour {} reset'.format(char)
        return colour


class Animation():
    def __init__(frames, speed):
        pass
