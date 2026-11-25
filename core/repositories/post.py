from abc import ABC, abstractmethod
from uuid import UUID

from core.models import Post


class PostRepo(ABC):
    """Interface para o repositório de artigos."""

    @abstractmethod
    def get_all(self) -> list[Post]:
        pass

    @abstractmethod
    def get_by_id(self, post_id: UUID | str) -> Post | None:
        pass

    @abstractmethod
    def get_highlighted(self) -> Post | None:
        pass

    @abstractmethod
    def create(self, post: Post) -> Post:
        pass

    @abstractmethod
    def update(self, post: Post) -> Post:
        pass

    @abstractmethod
    def delete(self, post_id: UUID | str) -> None:
        pass
