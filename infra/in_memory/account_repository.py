from core.models.account import Account
from core.repositories.account_repository import AccountRepository


class InMemoryAccountRepository(AccountRepository):
    def __init__(self):
        super().__init__()
        self.accounts = [
            Account(
                id="a4fbaf92-94cd-4e5f-ba21-bbc3955f8ccb",
                email="dev@gunther.com",
                hashed_password="$2b$12$og9VHSeyBtDceL0nINu5levdRVVZz.qQ.hZYX7SEUgaBzjAn3Mslm",
            )
        ]

    def find_by_email(self, email: str) -> Account | None:
        for account in self.accounts:
            if account.email == email:
                return account

        return None
