from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset


class Chixel():
    """Chixel: Character Pixel.
    Contains both character and colour information.

    TODO: Add unit tests for this class
    """
    def __init__(self, char, colour, mode='foreground'):
        self.char = char
        self.colour = colour
        self.mode = mode
        self.rendered = self._render()

    def _render(self):
        if self.colour:
            colour_code = rgb256(*self.colour)
            if self.mode == 'background':
                colour_code.replace('38', '48', 1)
            return ''.join([rgb256(*self.colour), self.char, str(reset)])
        else:
            return self.char

    def __repr__(self):
        return self.rendered
