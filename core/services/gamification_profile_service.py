from uuid import UUID

from core.exceptions.profile_exception import ProfileNotFoundError
from core.models.session import Session
from core.repositories.gamification_profile_repository import (
    GamificationProfileRepository,
)


class GamificationProfileService:
    def __init__(self, gamification_profile_repo: GamificationProfileRepository):
        self.gamification_profile_repo = gamification_profile_repo

    def get_by_profile_id(self, profile_id: UUID) -> Session | None:
        profile = self.gamification_profile_repo.get_by_profile_id(
            profile_id=profile_id
        )
        if not profile:
            raise ProfileNotFoundError()

        return profile
