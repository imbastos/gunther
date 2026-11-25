import config
from core.services import ArticleService, PostService, UserService
from core.services.auth import AuthService
from infra.db.sqlite import SqliteManager, initialize_database
from infra.repositories.sqlite import SqliteArticleRepo, SqlitePostRepo, SqliteUserRepo
from ui import TextualApp


def main():
    # Sqlite
    sqlite = SqliteManager(db_path=config.SQLITE_PATH)
    initialize_database(sqlite)

    # Repositórios
    user_repo = SqliteUserRepo(sqlite=sqlite)
    article_repo = SqliteArticleRepo(sqlite=sqlite)
    post_repo = SqlitePostRepo(sqlite=sqlite)

    # Serviços
    user_service = UserService(user_repo=user_repo)
    auth_service = AuthService(user_service=user_service)
    article_service = ArticleService(article_repo=article_repo)
    post_service = PostService(post_repo=post_repo)

    # Textual
    textual_app = TextualApp(
        auth_service=auth_service,
        user_service=user_service,
        article_service=article_service,
        post_service=post_service,
    )
    textual_app.run()


if __name__ == "__main__":
    main()
