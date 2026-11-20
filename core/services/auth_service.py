from core.exceptions.auth_exception import InvalidCredentialsError
from core.models.session import Session
from core.repositories.account_repository import AccountRepository
from utils.check_password import check_password


class AuthService:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    def signin_with_email(self, email: str, password: str) -> Session | None:
        found_account = self.account_repo.find_by_email(email=email)
        if not found_account:
            raise InvalidCredentialsError()

        is_credentials_valid = check_password(
            password=password, hashed_password=found_account.hashed_password
        )

        if not is_credentials_valid:
            raise InvalidCredentialsError()

        return Session(account=found_account)
