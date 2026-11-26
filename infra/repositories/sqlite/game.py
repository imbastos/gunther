from typing import Literal
from uuid import UUID

from core.models import Game
from core.repositories import GameRepo
from infra.db.sqlite.manager import SqliteManager

_GAME_COLUMNS = "id, name, description, difficulty, is_weekly"


def _row_to_game(row: tuple) -> Game:
    return Game(
        id=UUID(row[0]),
        name=row[1],
        description=row[2],
        difficulty=row[3],
        is_weekly=bool(row[4]),
    )


class SqliteGameRepo(GameRepo):
    """Implementação do repositório de jogos usando SQLite."""

    def __init__(self, sqlite: SqliteManager):
        self.sqlite = sqlite

    def _select(self, where_clause: str = "", params: tuple = ()) -> list[Game]:
        query = f"SELECT {_GAME_COLUMNS} FROM games"
        if where_clause:
            query += f" WHERE {where_clause}"
        query += " ORDER BY name ASC"

        with self.sqlite as db:
            results = db.fetch_all(query, params)

        return [_row_to_game(row) for row in results]

    def _select_one(self, where_clause: str, params: tuple) -> Game | None:
        query = f"SELECT {_GAME_COLUMNS} FROM games WHERE {where_clause}"
        with self.sqlite as db:
            result = db.fetch_one(query, params)

        return _row_to_game(result) if result else None

    def get_all(self) -> list[Game]:
        return self._select()

    def get_weekly(self) -> Game | None:
        return self._select_one("is_weekly = 1", ())

    def get_by_id(self, game_id: UUID | str) -> Game | None:
        return self._select_one("id = ?", (str(game_id),))

    def find_by_name(self, name: str) -> Game | None:
        return self._select_one("name = ?", (name,))

    def get_by_difficulty(self, difficulty: Literal[1, 2, 3]) -> list[Game]:
        return self._select("difficulty = ?", (int(difficulty),))

    def create(self, game: Game) -> Game:
        query = """
            INSERT INTO games (id, name, description, difficulty, is_weekly)
            VALUES (?, ?, ?, ?, ?)
        """
        with self.sqlite as db:
            db.execute(
                query,
                (
                    str(game.id),
                    game.name,
                    game.description,
                    game.difficulty,
                    int(bool(game.is_weekly)),
                ),
            )
        return game

    def update(self, game: Game) -> Game:
        query = """
            UPDATE games
            SET name = ?,
                description = ?,
                difficulty = ?,
                is_weekly = ?
            WHERE id = ?
        """
        with self.sqlite as db:
            db.execute(
                query,
                (
                    game.name,
                    game.description,
                    game.difficulty,
                    int(bool(game.is_weekly)),
                    str(game.id),
                ),
            )
        return game

    def delete(self, game_id: UUID | str) -> None:
        query = "DELETE FROM games WHERE id = ?"
        with self.sqlite as db:
            db.execute(query, (str(game_id),))
