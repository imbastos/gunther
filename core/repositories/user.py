from abc import ABC, abstractmethod

from core.models import User


class UserRepo(ABC):
    """Interface para o repositório de usuários"""

    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def create(self, data: dict) -> User:
        pass

    @abstractmethod
    def update(self, id: int, data: dict) -> User:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
