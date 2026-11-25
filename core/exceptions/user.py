from core.base import Error


class UserError(Error):
    """Erro relacionado a usuários."""


class UserNotFoundError(UserError):
    """Erro lançado quando o usuário não é encontrado."""

    def __init__(self, message: str = "Usuário não encontrado") -> None:
        super().__init__(message)
