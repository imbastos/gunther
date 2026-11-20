class ProfileException(Exception):
    """Erros relacionados à autenticação."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ProfileNotFoundError(ProfileException):
    """Exceção lançada quando o perfil não é encontrado."""

    def __init__(self, message: str = "Perfil não encontrado") -> None:
        super().__init__(message)
