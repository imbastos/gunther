from infra.db.sqlite.manager import SqliteManager


def initialize_database(sqlite_manager: SqliteManager):
    """Inicializa o schema do banco de dados."""

    create_users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            image TEXT,
            streak INTEGER NOT NULL DEFAULT 0,
            last_activity_at TEXT,
            completed_concepts TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL
        )
    """

    create_articles_table_query = """
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            area TEXT NOT NULL,
            parent_id TEXT,
            "order" INTEGER NOT NULL DEFAULT 0,
            introduction TEXT NOT NULL,
            explanation TEXT NOT NULL,
            examples TEXT NOT NULL DEFAULT '[]',
            "references" TEXT NOT NULL DEFAULT '[]',
            questions TEXT NOT NULL DEFAULT '[]',
            image TEXT,
            is_published INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            author TEXT NOT NULL,
            FOREIGN KEY (parent_id) REFERENCES articles(id) ON DELETE SET NULL
        )
    """

    create_posts_table_query = """
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            text TEXT NOT NULL DEFAULT '',
            image TEXT,
            is_highlighted INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """

    create_games_table_query = """
        CREATE TABLE IF NOT EXISTS games (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL DEFAULT '',
            difficulty INTEGER,
            is_weekly INTEGER NOT NULL DEFAULT 0
        )
    """

    with sqlite_manager as db:
        db.execute(create_users_table_query)
        db.execute(create_articles_table_query)
        db.execute(create_posts_table_query)
        db.execute(create_games_table_query)
