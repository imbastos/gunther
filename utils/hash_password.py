import bcrypt


def hash_password(password: str) -> str:
    """
    Criptografa a senha com salt
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    return hashed_password.decode("utf-8")
