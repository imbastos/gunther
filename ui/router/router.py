from textual.app import App

from core.exceptions.auth import NotAuthorizedError
from core.session import SessionManager


class Router:
    """Classe responsável por gerenciar as rotas"""

    def __init__(self, app: App, session_manager: SessionManager):
        self.app = app
        self.session_manager = session_manager

    def navigate_to(self, screen: str, **params):
        """Navega para uma tela com suporte a parâmetros de rota"""
        if screen not in self.app.SCREENS:
            raise ValueError(f"Tela '{screen}' não encontrada.")

        screen_cls = self.app.SCREENS[screen]
        if screen_cls.protected and not self.session_manager.is_authenticated:
            raise NotAuthorizedError()

        self.app.switch_screen(screen_cls(**params))
