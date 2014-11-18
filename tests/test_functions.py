import pytest
from textinator import build_lines, value_to_char, calculate_size


@pytest.fixture(scope='module')
def image():
    from PIL import Image
    im = Image.open('tests/images/doge.jpg')
    return im.convert('RGB')


@pytest.fixture(scope='module')
def expected_out():
    return open('tests/images/doge.txt')


def test_build_lines(image, expected_out):
    result_out = build_lines(image, '01', False, False)

    for expected_line, result_line in zip(expected_out, result_out):
        result_line += '\n'
        # click adds newlines later
        assert len(expected_line) == len(result_line)
        assert expected_line == result_line


def test_value_to_char():
    assert value_to_char((50, 200, 150), 'abcdef', colour=True) \
        == '\x1b[38;5;79md\x1b[0m'
    assert value_to_char((50, 200, 150), 'abcdef', colour=True, background=True) \
        == '\x1b[48;5;79md\x1b[0m'
    assert value_to_char([100]*3, 'abcdefghijk') == 'e'
    assert value_to_char([192]*3, 'abcdefghijk') == 'i'
    with pytest.raises(TypeError):
        value_to_char(200, 'abcdef')
        value_to_char((2, 4, 5, 6), 'abcdef')

def test_calculate_size():
        # Width know, height unknown
        assert calculate_size((1920, 1080), (20, None)) == (20, 11)
        assert calculate_size((500, 1240), (200, None)) == (200, 496)

        # Height known, width unknown
        assert calculate_size((1024, 768), (None, 413)) == (550, 413)
        assert calculate_size((10, 670), (None, 800)) == (11, 800)

        # Width and height known
        assert calculate_size((500, 600), (42, 612)) == (42, 612)
