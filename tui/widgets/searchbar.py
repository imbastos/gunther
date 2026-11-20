from textual.widget import Widget
from textual.widgets import Input, Static


class Searchbar(Widget):
    def compose(self):
        yield Input(placeholder="Procurar")
        yield Static("🔎︎", classes="icon")
