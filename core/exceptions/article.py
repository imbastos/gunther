from core.base import Error


class ArticleError(Error):
    """Erro relacionado a artigos."""


class NotFoundArticleError(ArticleError):
    """Erro lançado quando o artigo não é encontrado."""

    def __init__(self, message: str = "Artigo não encontrado") -> None:
        super().__init__(message)


class DuplicateArticleSlugError(ArticleError):
    """Erro lançado quando já existe um artigo com o mesmo slug."""

    def __init__(self, message: str = "Já existe um artigo com este slug") -> None:
        super().__init__(message)


class InvalidArticleHierarchyError(ArticleError):
    """Erro lançado quando a hierarquia do artigo é inválida."""

    def __init__(self, message: str = "Hierarquia de artigo inválida") -> None:
        super().__init__(message)
