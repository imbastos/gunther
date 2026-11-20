from abc import ABC, abstractmethod

from core.models.account import Account


class AccountRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Account | None:
        pass
