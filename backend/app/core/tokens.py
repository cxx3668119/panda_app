from uuid import uuid4


def generate_session_token() -> str:
    return uuid4().hex + uuid4().hex
