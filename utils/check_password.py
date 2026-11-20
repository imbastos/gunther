import bcrypt


def check_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha coincide com a senha criptografada
    """
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )
