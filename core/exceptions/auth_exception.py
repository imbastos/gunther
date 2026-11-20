class AuthException(Exception):
    """Erros relacionados à autenticação."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class InvalidCredentialsError(AuthException):
    """Exceção lançada quando as credenciais de autenticação são inválidas."""

    def __init__(self, message: str = "Credenciais inválidas") -> None:
        super().__init__(message)


class NotAuthorizedError(AuthException):
    """Exceção lançada quando o usuário não possui permissões para realizar uma atividade."""

    def __init__(self, message: str = "Não autorizado") -> None:
        super().__init__(message)
