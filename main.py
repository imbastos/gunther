from core.services.auth_service import AuthService
from core.services.gamification_profile_service import GamificationProfileService
from core.services.profile_service import ProfileService
from infra.in_memory.account_repository import InMemoryAccountRepository
from infra.in_memory.gamification_profile_repository import (
    InMemoryGamificationProfileRepository,
)
from infra.in_memory.profile_repository import InMemoryProfileRepository
from tui.app import TextualApp


def main():
    account_repo = InMemoryAccountRepository()
    profile_repo = InMemoryProfileRepository()
    gamification_profile_repo = InMemoryGamificationProfileRepository()

    auth_service = AuthService(account_repo=account_repo)
    profile_service = ProfileService(profile_repo=profile_repo)
    gamification_profile_service = GamificationProfileService(
        gamification_profile_repo=gamification_profile_repo
    )

    textual_app = TextualApp(auth_service=auth_service, profile_service=profile_service, gamification_profile_service=gamification_profile_service)
    textual_app.run()


if __name__ == "__main__":
    main()
