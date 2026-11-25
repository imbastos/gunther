from textual.containers import Horizontal
from textual.widget import Widget

from .profile import Profile
from .searchbar import Searchbar
from .streak import Streak


class Header(Widget):
    """Cabeçalho fixo superior das telas autenticadas."""

    def __init__(self, streak: int, **kwargs):
        super().__init__(classes="w-full h-5", **kwargs)
        self.streak = streak

    def compose(self):
        with Horizontal(classes="h-full w-full p-1-2"):
            yield Searchbar()
            yield Streak(streak=self.streak)
            yield Profile()
