from core.base import Error


class PostError(Error):
    """Erro relacionado a artigos da página inicial."""


class NotFoundPostError(PostError):
    """Erro lançado quando o artigo não é encontrado."""

    def __init__(self, message: str = "Artigo não encontrado") -> None:
        super().__init__(message)
