from abc import ABC, abstractmethod
from typing import Literal
from uuid import UUID

from core.models import Game


class GameRepo(ABC):
    """Interface para o repositório de jogos."""

    @abstractmethod
    def get_all(self) -> list[Game]:
        pass

    @abstractmethod
    def get_weekly(self) -> Game | None:
        pass

    @abstractmethod
    def get_by_id(self, game_id: UUID | str) -> Game | None:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Game | None:
        pass

    @abstractmethod
    def get_by_difficulty(self, difficulty: Literal[1, 2, 3]) -> list[Game]:
        pass

    @abstractmethod
    def create(self, game: Game) -> Game:
        pass

    @abstractmethod
    def update(self, game: Game) -> Game:
        pass

    @abstractmethod
    def delete(self, game_id: UUID | str) -> None:
        pass