from textual.widgets import Static

from tui.widgets.modal import Modal


class ProfileModal(Modal):
    def __init__(self):
        actions = {
            "profile": lambda: self.app.navigate("profile"),
            "signout": self.handle_signout,
        }
        super().__init__(actions)

    def compose(self):
        yield Static("Perfil", id="profile", classes="action")
        yield Static("Configurações", classes="action")
        yield Static("Sair", id="signout", classes="action caution")
