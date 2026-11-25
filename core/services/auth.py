import utils
from core.exceptions.auth import InvalidCredentialsError
from core.models import Session, User
from core.services.user import UserService


class AuthService:
    """Serviço responsável pela autenticação de usuários."""

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def signup(self, username: str, email: str, password: str) -> User:
        user = User(
            name="Sem nome",
            username=username,
            email=email,
            hashed_password=utils.hash_password(password),
        )

        return self.user_service.create(user)

    def signin(self, email: str, password: str) -> Session:
        user = self.user_service.find_by_email(email)

        if not utils.check_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        return Session(user_id=user.id)
