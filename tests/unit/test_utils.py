import pytest
from mistakes import NotFound
from utils import build_path, read_static
from chek import to_bytes

from custom_types import HttpRequest


def test_build_path():
    original = [

        "/",
        "/xxx",
        "/hello",
    ]
    expected = [

        "/",
        "/xxx/",
        "/hello/",
    ]
    for i in range(len(original)):
        t = original[i]
        e = expected[i]
        got = build_path(t)
        assert got == e, f"path {t} normolized to {got}, while {e} expected"


def test_to_bytes():
    original = [
        "xxx",
        b"hello",
    ]

    expected = [
        b"xxx",
        b"hello",
    ]
    for i in range(len(original)):
        t = original[i]
        e = expected[i]
        got = to_bytes(t)
        assert got == e, f"path {t} normolized to {got}, while {e} expected"



def test_endpoint():
    data_set = {
        "": HttpRequest(original="", normal="/", file_name=None),
        "/": HttpRequest(original="/", normal="/", file_name=None),
        "/images": HttpRequest(original="/images", normal="/images/", file_name=None),
        "/images/": HttpRequest(original="/images/", normal="/images/", file_name=None),
        "/images/a": HttpRequest(
            original="/images/a", normal="/images/a/", file_name=None
        ),
        "/images/a/": HttpRequest(
            original="/images/a/", normal="/images/a/", file_name=None
        ),
        "/images/image.jpg": HttpRequest(
            original="/images/image.jpg", normal="/images/", file_name="image.jpg"
        ),
        "/images/image.png/": HttpRequest(
            original="/images/image.png/", normal="/images/", file_name="image.png"
        ),
        "/images/x/image.jpg": HttpRequest(
            original="/images/x/image.jpg", normal="/images/x/", file_name="image.jpg"
        ),
        "/images/x/image.jpg/": HttpRequest(
            original="/images/x/image.jpg/", normal="/images/x/", file_name="image.jpg"
        ),
    }

    for path, expected_endpoint in data_set.items():
        got_endpoint = HttpRequest.from_path(path)

        assert (
                got_endpoint == expected_endpoint
        ), f"mismatch for `{path}`: expected {expected_endpoint}, got {got_endpoint}"