from abc import ABC, abstractmethod
from uuid import UUID

from core.models.profile import Profile


class ProfileRepository(ABC):
    @abstractmethod
    def get_by_account_id(self, account_id: UUID) -> Profile | None:
        pass
