from typing import TYPE_CHECKING

from textual.screen import Screen

from core.exceptions.user import UserNotFoundError
from core.models import User
from core.services import ArticleService, AuthService, PostService, UserService
from core.session import SessionManager

if TYPE_CHECKING:
    from ui.router import Router


class BaseScreen(Screen):
    """Classe base para todas as telas do aplicativo"""
    protected = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.auth_service: AuthService = self.app.auth_service
        self.user_service: UserService = self.app.user_service
        self.article_service: ArticleService | None = self.app.article_service
        self.post_service: PostService | None = self.app.post_service

        self.session_manager: SessionManager = self.app.session_manager
        self.router: Router = self.app.router

    @property
    def current_user(self) -> User | None:
        """Retorna o usuário autenticado na sessão atual, se existir."""
        session = self.session_manager.current_session
        if session is None or self.user_service is None:
            return None
        try:
            return self.user_service.get_by_id(session.user_id)
        except UserNotFoundError:
            return None

    @property
    def is_admin(self) -> bool:
        """Indica se o usuário atual possui a role admin."""
        user = self.current_user
        return user is not None and user.role == "admin"
