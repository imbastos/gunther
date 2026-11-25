import json
from datetime import datetime

from core.exceptions.user import UserNotFoundError
from core.models import User
from core.repositories import UserRepo
from infra.db.sqlite.manager import SqliteManager

_COLUMNS = (
    "id, name, username, email, role, image, streak, last_activity_at, "
    "completed_concepts, created_at"
)


def _to_user(row: tuple, with_password: bool = False) -> User:
    if with_password:
        return User(
            id=row[0],
            name=row[1],
            username=row[2],
            email=row[3],
            hashed_password=row[4],
            role=row[5],
            image=row[6],
            streak=int(row[7] or 0),
            last_activity_at=row[8],
            completed_concepts=_parse_concepts(row[9]),
            created_at=row[10],
        )

    return User(
        id=row[0],
        name=row[1],
        username=row[2],
        email=row[3],
        role=row[4],
        image=row[5],
        streak=int(row[6] or 0),
        last_activity_at=row[7],
        completed_concepts=_parse_concepts(row[8]),
        created_at=row[9],
    )


def _parse_concepts(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        result = json.loads(value)
        return [str(item) for item in result] if isinstance(result, list) else []
    except (ValueError, TypeError):
        return []


def _date_value(value: datetime | str | None) -> str | None:
    if value is None:
        return None
    return value.isoformat() if isinstance(value, datetime) else str(value)


class SqliteUserRepo(UserRepo):
    """Repositório de usuários usando SQLite."""

    def __init__(self, sqlite: SqliteManager):
        self.sqlite = sqlite

    def get_all(self) -> list[User]:
        with self.sqlite as db:
            rows = db.fetch_all(f"SELECT {_COLUMNS} FROM users")
        return [_to_user(row) for row in rows]

    def get_by_id(self, user_id: str) -> User | None:
        with self.sqlite as db:
            row = db.fetch_one(
                f"SELECT {_COLUMNS} FROM users WHERE id = ?", (str(user_id),)
            )
        if not row:
            raise UserNotFoundError()
        return _to_user(row)

    def find_by_email(self, email: str) -> User:
        query = """
            SELECT id, name, username, email, hashed_password, role, image,
                   streak, last_activity_at, completed_concepts, created_at
            FROM users WHERE email = ?
        """
        with self.sqlite as db:
            row = db.fetch_one(query, (email,))
        if not row:
            raise UserNotFoundError()
        return _to_user(row, with_password=True)

    def create(self, user: User) -> User:
        query = """
            INSERT INTO users (
                id, name, username, email, hashed_password, role, image,
                streak, last_activity_at, completed_concepts, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            str(user.id),
            user.name,
            user.username,
            user.email,
            user.hashed_password,
            user.role,
            user.image,
            int(user.streak),
            _date_value(user.last_activity_at),
            json.dumps(user.completed_concepts),
            user.created_at,
        )
        with self.sqlite as db:
            db.execute(query, params)
        return user

    def update(self, user: User) -> User:
        fields = [
            "name = ?",
            "username = ?",
            "email = ?",
            "role = ?",
            "image = ?",
            "streak = ?",
            "last_activity_at = ?",
            "completed_concepts = ?",
        ]
        params = [
            user.name,
            user.username,
            user.email,
            user.role,
            user.image,
            int(user.streak),
            _date_value(user.last_activity_at),
            json.dumps(user.completed_concepts),
        ]
        if user.hashed_password is not None:
            fields.append("hashed_password = ?")
            params.append(user.hashed_password)

        params.append(str(user.id))
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        with self.sqlite as db:
            db.execute(query, tuple(params))
        return user

    def delete(self, user_id: str) -> None:
        with self.sqlite as db:
            db.execute("DELETE FROM users WHERE id = ?", (str(user_id),))
