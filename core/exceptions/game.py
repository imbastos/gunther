from core.base import Error


class GameError(Error):
    """Erro relacionado a jogos."""


class NotFoundGameError(GameError):
    """Erro lançado quando o jogo não é encontrado."""

    def __init__(self, message: str = "Jogo não encontrado") -> None:
        super().__init__(message)


class DuplicateGameNameError(GameError):
    """Erro lançado quando já existe um jogo com o mesmo nome."""

    def __init__(self, message: str = "Já existe um jogo com este nome") -> None:
        super().__init__(message)
