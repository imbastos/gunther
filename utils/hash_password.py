from bcrypt import gensalt, hashpw


def hash_password(password: str) -> str:
    """Criptografa a senha usando bcrypt"""
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
