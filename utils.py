from typing import AnyStr
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

def to_str(text: AnyStr) -> str:

    result = text

    if not isinstance(text, (str, bytes)):
        result = str(text)

    if isinstance(result, bytes):
        result = result.decode()

    return result