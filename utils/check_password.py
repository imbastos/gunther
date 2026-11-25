from bcrypt import checkpw


def check_password(password: str, hashed_password: str) -> str:
    """Verifica se a senha é válida usando bcrypt"""
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
