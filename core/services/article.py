from uuid import UUID

import utils
from core.exceptions.article import (
    DuplicateArticleSlugError,
    InvalidArticleHierarchyError,
    NotFoundArticleError,
)
from core.models import Article, ArticleArea
from core.repositories import ArticleRepo


class ArticleService:
    """Serviço responsável pelo gerenciamento de artigos."""

    def __init__(self, article_repo: ArticleRepo):
        self.article_repo = article_repo

    def _validate_slug(self, article: Article) -> None:
        existing = self.article_repo.find_by_slug(article.slug)

        if existing and existing.id != article.id:
            raise DuplicateArticleSlugError()

    def _validate_parent(self, article: Article) -> None:
        if article.parent_id is None:
            return

        if article.parent_id == article.id:
            raise InvalidArticleHierarchyError()

        if self.article_repo.get_by_id(article.parent_id) is None:
            raise NotFoundArticleError()

    def get_all(self) -> list[Article]:
        return self.article_repo.get_all()

    def get_published(self) -> list[Article]:
        return self.article_repo.get_published()

    def get_by_id(self, article_id: UUID | str) -> Article:
        article = self.article_repo.get_by_id(article_id)

        if article is None:
            raise NotFoundArticleError()

        return article

    def find_by_slug(self, slug: str) -> Article:
        article = self.article_repo.find_by_slug(slug)

        if article is None:
            raise NotFoundArticleError()

        return article

    def get_by_area(self, area: ArticleArea | str) -> list[Article]:
        return self.article_repo.get_by_area(area)

    def get_children(self, parent_id: UUID | str | None) -> list[Article]:
        return self.article_repo.get_children(parent_id)

    def create(self, article: Article) -> Article:
        self._validate_slug(article)
        self._validate_parent(article)

        return self.article_repo.create(article)

    def update(self, article: Article) -> Article:
        self.get_by_id(article.id)
        self._validate_slug(article)
        self._validate_parent(article)

        article.updated_at = utils.date_now()
        return self.article_repo.update(article)

    def publish(self, article_id: UUID | str) -> Article:
        article = self.get_by_id(article_id)
        article.is_published = True

        return self.update(article)

    def unpublish(self, article_id: UUID | str) -> Article:
        article = self.get_by_id(article_id)
        article.is_published = False

        return self.update(article)

    def delete(self, article_id: UUID | str) -> None:
        self.get_by_id(article_id)
        self.article_repo.delete(article_id)
