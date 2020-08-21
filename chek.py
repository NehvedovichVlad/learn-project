def to_bytes(message):
    if isinstance(message, bytes):
        return message

    if not isinstance(message, str):
        msg = f'cannot convert {type(message)} to bytes'
        raise ValueError(msg)
    message = message.encode()
    return message

