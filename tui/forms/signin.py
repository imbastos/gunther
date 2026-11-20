from textual.message import Message
from textual.validation import Length, Regex
from textual.widgets import Button

from core.exceptions.auth_exception import AuthException
from core.services.auth_service import AuthService
from tui.widgets.form import Form
from tui.widgets.form_field import FormField


class SigninForm(Form):
    def __init__(self, auth_service: AuthService, message: Message):
        super().__init__()
        self.auth_service = auth_service
        self.message = message

    def compose(self):
        yield FormField(
            placeholder="Email",
            id="email",
            validators=[
                Regex(
                    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                    failure_description="formato inválido",
                ),
                Length(
                    minimum=8,
                    failure_description="tamanho inválido",
                ),
            ],
        )
        yield FormField(
            placeholder="Senha",
            id="password",
            password=True,
            validators=[
                Length(
                    minimum=8,
                    failure_description="tamanho inválido",
                ),
            ],
        )
        yield Button("Entrar", classes="submit")

    def on_submit(self):
        email = self.query_one("#email", FormField).value.strip()
        password = self.query_one("#password", FormField).value

        try:
            session = self.auth_service.signin_with_email(
                email=email,
                password=password,
            )

            self.notify(f"Entrou em {session.account.email}")
            self.post_message(self.message(session=session))
        except AuthException as e:
            self.notify(e.message, severity="error")
