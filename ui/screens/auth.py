from textual.containers import Container
from textual.widgets import Static, TabbedContent, TabPane

from core.exceptions.auth import AuthError
from core.exceptions.user import UserError
from ui.base.screen import BaseScreen
from ui.forms import auth_fields
from ui.widgets.form import Form
from ui.widgets.form.field import FormField


class AuthScreen(BaseScreen):
    """Tela de autenticação do aplicativo"""

    def compose(self):
        signin = AuthPane(
            title="Entrar",
            heading="Entre com a sua conta",
            handle_signin=self.handle_signin,
            fields=[auth_fields.email(), auth_fields.password()],
        )
        signup = AuthPane(
            title="Cadastrar",
            heading="Crie uma nova conta",
            handle_signin=self.handle_signup,
            fields=[auth_fields.username(), auth_fields.email(), auth_fields.password()],
        )

        with (
            Container(classes="center-container"),
            Container(classes="content-container w-1--3"),
            TabbedContent(classes="round-surface w-1--1"),
        ):
            yield signin
            yield signup

    def handle_signin(self, data: dict):
        try:
            session = self.auth_service.signin(
                email=data["email"],
                password=data["password"],
            )

            self.session_manager.start(user_id=session.user_id)
            self.router.navigate_to("home")
        except (AuthError, UserError) as e:
            self.app.notify(e.message, severity="error")

    def handle_signup(self, data: dict):
        try:
            user = self.auth_service.signup(
                username=data["username"],
                email=data["email"],
                password=data["password"],
            )

            self.session_manager.start(user_id=user.id)
            self.router.navigate_to("onboarding")
        except AuthError as e:
            self.app.notify(e.message, severity="error")


class AuthPane(TabPane):
    def __init__(
        self,
        title: str,
        heading: str,
        handle_signin: callable,
        fields: list[FormField],
        classes="",
    ):
        super().__init__(title=title, classes=classes)
        self.handle_signin = handle_signin
        self.fields = fields
        self.heading = heading

    def compose(self):
        title = Static(self.heading, classes="text-bold text-center p-1-2")
        form = Form(
            fields=self.fields,
            on_submit=self.handle_signin,
            submit_message="Entrar",
        )

        yield title
        yield form


# class SignupPane(TabPane):
#     def compose(self):
#         yield Form(fields=(FormField(),))
