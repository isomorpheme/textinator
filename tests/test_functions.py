import pytest
import textinator


@pytest.fixture
def image():
    from PIL import Image
    im = Image.open('images/doge.jpg')
    return im


@pytest.fixture
def expected_out():
    return open('images/doge.txt')


def test_build_lines(image, expected_out):
    result_out = textinator.build_lines(image, '01', False, False)

    assert len(expected_out) == len(result_out)
    for expected_line, result_line in zip(expected_out, result_out):
        assert expected_line == result_line


def test_value_to_char():
    from textinator import value_to_char

    assert value_to_char(50, 'abc', value_range=(0, 100)) == 'b'
    assert value_to_char(100, 'abcdefghijk') == 'e'
    assert value_to_char(192, 'abcdefghijk') == 'i'
    with pytest.raises(ValueError):
        value_to_char(260, 'abcdef')
        value_to_char(200, 'abcdef', value_range=(0, 200))
        # yes, that should return an error. value_range is non inclusive
