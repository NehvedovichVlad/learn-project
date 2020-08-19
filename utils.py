def build_path(path) -> str:
    result = path
    if result[-1] != "/":
        result = f"{result}/"
    return result