from uuid import UUID

from core.models.profile import Profile
from core.repositories.profile_repository import ProfileRepository


class InMemoryProfileRepository(ProfileRepository):
    def __init__(self):
        super().__init__()
        self.profiles = [
            Profile(
                id="18bbd9fd-5da4-4a22-9f7f-3a50f28d62eb",
                account_id="a4fbaf92-94cd-4e5f-ba21-bbc3955f8ccb",
                display_name="Desenvolvedor",
                username="dev_account",
                photo="assets/icon.png",
            )
        ]

    def get_by_account_id(self, account_id: UUID) -> Profile | None:
        for profile in self.profiles:
            if profile.account_id == account_id:
                return profile

        return None
