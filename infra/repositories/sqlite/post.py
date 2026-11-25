from datetime import datetime
from uuid import UUID

from core.models import Post
from core.repositories import PostRepo
from infra.db.sqlite.manager import SqliteManager

_COLUMNS = "id, name, text, image, is_highlighted, created_at, updated_at"


def _to_post(row: tuple) -> Post:
    return Post(
        id=UUID(row[0]),
        name=row[1],
        text=row[2],
        image=row[3],
        is_highlighted=bool(row[4]),
        created_at=row[5],
        updated_at=row[6],
    )


def _date_value(value: datetime | str) -> str:
    return value.isoformat() if isinstance(value, datetime) else str(value)


class SqlitePostRepo(PostRepo):
    """Repositório de posts usando SQLite."""

    def __init__(self, sqlite: SqliteManager):
        self.sqlite = sqlite

    def get_all(self) -> list[Post]:
        query = f"SELECT {_COLUMNS} FROM posts ORDER BY is_highlighted DESC, created_at DESC"
        with self.sqlite as db:
            rows = db.fetch_all(query)
        return [_to_post(row) for row in rows]

    def get_by_id(self, post_id: UUID | str) -> Post | None:
        with self.sqlite as db:
            row = db.fetch_one(
                f"SELECT {_COLUMNS} FROM posts WHERE id = ?", (str(post_id),)
            )
        return _to_post(row) if row else None

    def get_highlighted(self) -> Post | None:
        query = f"SELECT {_COLUMNS} FROM posts WHERE is_highlighted = 1 ORDER BY created_at, id LIMIT 1"
        with self.sqlite as db:
            row = db.fetch_one(query)
        return _to_post(row) if row else None

    def create(self, post: Post) -> Post:
        query = """
            INSERT INTO posts (id, name, text, image, is_highlighted, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            str(post.id),
            post.name,
            post.text,
            post.image,
            int(bool(post.is_highlighted)),
            _date_value(post.created_at),
            _date_value(post.updated_at),
        )
        with self.sqlite as db:
            db.execute(query, params)
        return post

    def update(self, post: Post) -> Post:
        query = """
            UPDATE posts SET name = ?, text = ?, image = ?,
                is_highlighted = ?, updated_at = ?
            WHERE id = ?
        """
        params = (
            post.name,
            post.text,
            post.image,
            int(bool(post.is_highlighted)),
            _date_value(post.updated_at),
            str(post.id),
        )
        with self.sqlite as db:
            db.execute(query, params)
        return post

    def delete(self, post_id: UUID | str) -> None:
        with self.sqlite as db:
            db.execute("DELETE FROM posts WHERE id = ?", (str(post_id),))
