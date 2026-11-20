from textual.containers import Container
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Static

from core.models.session import Session
from core.services.auth_service import AuthService
from tui.forms.signin import SigninForm


class AuthScreen(Screen):
    class Authenticated(Message):
        """Emitida quando o usuário autentica com sucesso."""

        def __init__(self, session: Session) -> None:
            super().__init__()
            self.session = session

    def __init__(self, auth_service: AuthService):
        super().__init__()

        self.auth_service = auth_service

    def compose(self):
        with Container():
            yield Static("Fazer Login")
            yield SigninForm(auth_service=self.auth_service, message=self.Authenticated)
