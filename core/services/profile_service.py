from uuid import UUID

from core.exceptions.profile_exception import ProfileNotFoundError
from core.models.session import Session
from core.repositories.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, profile_repo: ProfileRepository):
        self.profile_repo = profile_repo

    def get_by_account_id(self, account_id: UUID) -> Session | None:
        profile = self.profile_repo.get_by_account_id(account_id=account_id)
        if not profile:
            raise ProfileNotFoundError()

        return profile
