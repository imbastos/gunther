from core.base import Error


class DatabaseError(Error):
    """Erro relacionado a banco de dados"""


class DatabaseConnectionError(DatabaseError):
    """Erro relacionado a conexão com o banco de dados"""

    def __init__(self, message: str = "Falha ao conectar ao banco de dados") -> None:
        super().__init__(message)
