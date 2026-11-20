from textual.widget import Widget

from tui.widgets.profile import Profile
from tui.widgets.searchbar import Searchbar
from tui.widgets.streak import Streak


class Header(Widget):
    def compose(self):
        yield Searchbar()
        yield Streak()
        yield Profile()
