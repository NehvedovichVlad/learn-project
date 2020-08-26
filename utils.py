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
    static = settings.STATIC_DIR / path
    if not static.is_file():
        full_path = static.resolve().as_posix()
        msg = f"file <{full_path}> not found "
        raise NotFound(msg)

    with static.open("rb") as fp:
        result = fp.read()

    return result
