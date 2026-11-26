from typing import Literal
from uuid import UUID

from core.exceptions.game import (
    DuplicateGameNameError,
    NotFoundGameError,
)
from core.models import Game
from core.repositories import GameRepo


class GameService:
    """Serviço responsável pelo gerenciamento de jogos."""

    def __init__(self, game_repo: GameRepo):
        self.game_repo = game_repo

    def _validate_name(self, game: Game) -> None:
        existing = self.game_repo.find_by_name(game.name)

        if existing and existing.id != game.id:
            raise DuplicateGameNameError()

    def _unset_current_weekly(self, except_id: UUID | None = None) -> None:
        current_weekly = self.game_repo.get_weekly()

        if current_weekly and current_weekly.id != except_id:
            current_weekly.is_weekly = False
            self.game_repo.update(current_weekly)

    def get_all(self) -> list[Game]:
        return self.game_repo.get_all()

    def get_weekly(self) -> Game | None:
        return self.game_repo.get_weekly()

    def get_by_id(self, game_id: UUID | str) -> Game:
        game = self.game_repo.get_by_id(game_id)

        if game is None:
            raise NotFoundGameError()

        return game

    def find_by_name(self, name: str) -> Game:
        game = self.game_repo.find_by_name(name)

        if game is None:
            raise NotFoundGameError()

        return game

    def get_by_difficulty(self, difficulty: Literal[1, 2, 3]) -> list[Game]:
        return self.game_repo.get_by_difficulty(difficulty)

    def create(self, game: Game) -> Game:
        self._validate_name(game)

        if game.is_weekly:
            self._unset_current_weekly()

        return self.game_repo.create(game)

    def update(self, game: Game) -> Game:
        self.get_by_id(game.id)
        self._validate_name(game)

        if game.is_weekly:
            self._unset_current_weekly(except_id=game.id)

        return self.game_repo.update(game)

    def set_weekly(self, game_id: UUID | str) -> Game:
        game = self.get_by_id(game_id)

        if game.is_weekly:
            return game

        self._unset_current_weekly(except_id=game.id)
        game.is_weekly = True

        return self.game_repo.update(game)

    def unset_weekly(self, game_id: UUID | str) -> Game:
        game = self.get_by_id(game_id)
        game.is_weekly = False

        return self.game_repo.update(game)

    def delete(self, game_id: UUID | str) -> None:
        self.get_by_id(game_id)
        self.game_repo.delete(game_id)
