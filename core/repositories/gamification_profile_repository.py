from abc import ABC, abstractmethod
from uuid import UUID

from core.models.gamification_profile import GamificationProfile


class GamificationProfileRepository(ABC):
    @abstractmethod
    def get_by_profile_id(self, profile_id: UUID) -> GamificationProfile | None:
        pass
