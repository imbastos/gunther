from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Label


class Store(Widget):
    def __init__(self):
        super().__init__(
            classes="w-1--3 m-1 h-full",
        )

    def compose(self):
        with Container(classes="round-surface p-1 w-full h-full"):
            yield Label("Loja")
