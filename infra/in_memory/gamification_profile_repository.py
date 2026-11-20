from uuid import UUID

from core.models.gamification_profile import GamificationProfile
from core.repositories.gamification_profile_repository import (
    GamificationProfileRepository,
)


class InMemoryGamificationProfileRepository(GamificationProfileRepository):
    def __init__(self):
        super().__init__()
        self.gamification_profiles = [
            GamificationProfile(
                profile_id="18bbd9fd-5da4-4a22-9f7f-3a50f28d62eb",
                streak=1
            )
        ]

    def get_by_profile_id(self, profile_id: UUID) -> GamificationProfile | None:
        for gamification_profile in self.gamification_profiles:
            if gamification_profile.profile_id == profile_id:
                return gamification_profile

        return None
