from textual.screen import Screen
from textual.widgets import Static


class NotFoundScreen(Screen):
    def compose(self):
        yield Static("Página não encontrada")
