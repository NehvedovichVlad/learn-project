import mimetypes
from urllib.parse import parse_qs

from consts import ANONYMOUS_USER
from custom_types import User
from mistakes import NotFound
from typing import Union
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
    try:
        key_value_pairs = parse_qs(query, strict_parsing=True)
    except ValueError:
        return ANONYMOUS_USER

    name_values = key_value_pairs.get("name", [ANONYMOUS_USER.name])
    name = name_values[0]

    age_values = key_value_pairs.get("age", [ANONYMOUS_USER.age])
    age = age_values[0]
    if isinstance(age, str) and age.isdecimal():
        age = int(age)

    return User(name=name, age=age)