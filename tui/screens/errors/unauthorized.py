from textual.screen import Screen
from textual.widgets import Static


class UnauthorizedScreen(Screen):
    def compose(self):
        yield Static("Acesso negado")
