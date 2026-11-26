import json

import config
import utils
from infra.db.sqlite.dataset import articles, katas, posts
from infra.db.sqlite.manager import SqliteManager
from infra.db.sqlite.schema import initialize_database


def seed_database(sqlite_manager: SqliteManager) -> None:
    """Popula o banco de dados com dados iniciais."""
    admin_user = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Isaac Bastos",
        "username": "sooitaa",
        "email": "isaac@gunther.com",
        "hashed_password": utils.hash_password("password123"),
        "role": "admin",
        "created_at": "2026-08-10",
    }

    formatted_articles = [
        {
            **article,
            "examples": json.dumps(article["examples"]),
            "references": json.dumps(article["references"]),
            "questions": json.dumps(article.get("questions", [])),
            "created_at": "2026-11-25",
            "updated_at": "2026-11-25",
            "author": "sooitaa",
        }
        for article in articles
    ]

    formatted_posts = [
        {
            "id": str(post.id),
            "name": post.name,
            "text": post.text,
            "image": post.image,
            "is_highlighted": int(post.is_highlighted),
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
        for post in posts
    ]

    formatted_katas = [
        {
            "id": kata.id,
            "name": kata.name,
            "description": kata.description,
            "difficulty": kata.difficulty,
            "is_weekly": int(kata.is_weekly),
        }
        for kata in katas
    ]

    with sqlite_manager as db:
        db.insert_many("users", [admin_user])
        db.insert_many("articles", formatted_articles)
        db.insert_many("posts", formatted_posts)
        db.insert_many("games", formatted_katas)


if __name__ == "__main__":
    sqlite_manager = SqliteManager(db_path=config.SQLITE_PATH)

    initialize_database(sqlite_manager)
    seed_database(sqlite_manager)
