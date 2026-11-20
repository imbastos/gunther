from textual.widgets import Static

from tui.screens.templates.shell import Shell


class ProfileScreen(Shell):
    def __init__(self):
        super().__init__(protected=True, group="profile")

    def compose(self):
        yield from super().compose()
        yield Static(self.app.profile.display_name)
