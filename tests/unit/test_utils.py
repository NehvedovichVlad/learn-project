from utils import  build_path
from chek import to_bytes

def test_build_path():
    original=[

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
