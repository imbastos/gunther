from core.base import Error


class AuthError(Error):
    """Erro relacionado a autenticação."""


class InvalidCredentialsError(AuthError):
    """Exceção lançada quando as credenciais de autenticação são inválidas."""

    def __init__(self, message: str = "Credenciais inválidas") -> None:
        super().__init__(message)


class NotAuthorizedError(AuthError):
    """Erro lançado quando o usuário não possui permissões para realizar uma atividade."""

    def __init__(self, message: str = "Não autorizado") -> None:
        super().__init__(message)


class EmailAlreadyInUseError(AuthError):
    """Erro lançado quando o email já estiver sendo utilizado."""

    def __init__(self, message: str = "O e-mail informado já está em uso"):
        super().__init__()
