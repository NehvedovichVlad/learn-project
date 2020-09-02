import pytest

from custom_types import HttpRequest


@pytest.mark.unit
def test_endpoint():
    data_set = {
        "": HttpRequest(original="", normal="/"),
        "/": HttpRequest(original="/", normal="/"),
        "/images": HttpRequest(original="/images", normal="/images/"),
        "/images/": HttpRequest(original="/images/", normal="/images/"),
        "/images/a": HttpRequest(original="/images/a", normal="/images/a/"),
        "/images/a/": HttpRequest(original="/images/a/", normal="/images/a/"),
        "/images/image.jpg": HttpRequest(
            original="/images/image.jpg", normal="/images/", file_name="image.jpg"
        ),
        "/images/image.jpg/": HttpRequest(
            original="/images/image.jpg/", normal="/images/", file_name="image.jpg"
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