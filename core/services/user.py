import utils
from core.exceptions.user import UserNotFoundError
from core.models.user import User
from core.repositories.user import UserRepo


class UserService:
    """Serviço responsável pelo gerenciamento de usuários."""

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def get_all(self) -> list[User]:
        return self.user_repo.get_all()

    def create(self, user: User) -> User:
        return self.user_repo.create(user)

    def find_by_email(self, email: str) -> User:
        return self.user_repo.find_by_email(email)

    def get(self, user_id: int) -> User:
        return self.user_repo.get_by_id(str(user_id))

    def get_by_id(self, user_id) -> User | None:
        return self.user_repo.get_by_id(str(user_id))

    def update(self, user: User) -> User:
        return self.user_repo.update(user)

    def get_effective_streak(self, user: User | None, now=None) -> int:
        if user is None:
            return 0

        return utils.calculate_streak(
            user.streak,
            user.last_activity_at,
            now,
        )

    def complete_concept(self, user_id, concept_id, now=None) -> User:
        user = self.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        concept_id = str(concept_id)

        if concept_id not in user.completed_concepts:
            current = now or utils.date_now()

            user.streak = utils.calculate_streak(
                user.streak,
                user.last_activity_at,
                current,
            )

            user.last_activity_at = current
            user.completed_concepts.append(concept_id)

            self.user_repo.update(user)

        return user

    def uncomplete_concept(self, user_id, concept_id) -> User:
        user = self.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        concept_id = str(concept_id)

        if concept_id in user.completed_concepts:
            user.completed_concepts.remove(concept_id)
            self.user_repo.update(user)

        return user

    def delete(self, user_id: int) -> None:
        self.user_repo.delete(user_id)
