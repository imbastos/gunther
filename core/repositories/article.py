from abc import ABC, abstractmethod
from uuid import UUID

from core.models import Article, ArticleArea


class ArticleRepo(ABC):
    """Interface para o repositório de artigos."""

    @abstractmethod
    def get_all(self) -> list[Article]:
        pass

    @abstractmethod
    def get_published(self) -> list[Article]:
        pass

    @abstractmethod
    def get_by_id(self, article_id: UUID | str) -> Article | None:
        pass

    @abstractmethod
    def find_by_slug(self, slug: str) -> Article | None:
        pass

    @abstractmethod
    def get_by_area(self, area: ArticleArea | str) -> list[Article]:
        pass

    @abstractmethod
    def get_children(self, parent_id: UUID | str | None) -> list[Article]:
        pass

    @abstractmethod
    def create(self, article: Article) -> Article:
        pass

    @abstractmethod
    def update(self, article: Article) -> Article:
        pass

    @abstractmethod
    def delete(self, article_id: UUID | str) -> None:
        pass
