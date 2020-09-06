import mimetypes
from urllib.parse import parse_qs
from typing import AnyStr
from custom_types import User
from mistakes import NotFound
import settings


def build_path(path: str) -> str:
    if not path:
        return "/"

    result = path

    if result[-1] != "/":
        result = f"{result}/"
    return result


def read_static(path: str) -> bytes:
    static_obj = settings.STATIC_DIR / path
    if not static_obj.is_file():
        static_path = static_obj.resolve().as_posix()
        err_msg = f"file <{static_path}> not found"
        raise NotFound(err_msg)

    with static_obj.open("rb") as src:
        content = src.read()

    return content


def get_content_type(file_path: str) -> str:
    if not file_path:
        return "text/html"
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type


def get_user_data(query: str) -> User:
    from custom_types import User
    anonymous = User.default()

    try:
        key_value_pairs = parse_qs(query, strict_parsing=True)
    except ValueError:
        return anonymous

    name_values = key_value_pairs.get("name", [anonymous.name])
    name = name_values[0]
    age_values = key_value_pairs.get("age", [anonymous.age])
    age = age_values[0]

    errors = {}

    if not name_valid(name):
        errors["name"] = "name not valid"

    if not age_valid(age):
        errors["age"] = "age not valid"

    if errors:
        raise ValueError

    age = int(age)

    return User(name=name, age=age)


def to_str(text: AnyStr) -> str:
    """
    Safely converts any string to str.
    :param text: any string
    :return: str
    """

    result = text

    if not isinstance(text, (str, bytes)):
        result = str(text)

    if isinstance(result, bytes):
        result = result.decode()

    return result