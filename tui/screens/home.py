from textual.widgets import Static

from tui.screens.templates.shell import Shell
from tui.widgets.title import Title


class HomeScreen(Shell):
    def __init__(self):
        super().__init__(protected=True, group="home")

    def compose(self):
        yield from super().compose()
        yield Title("Inicio")
