from tui.modals.profile_modal import ProfileModal
from tui.screens.screen import Screen
from tui.widgets.header import Header
from tui.widgets.sidebar import Sidebar


class Shell(Screen):
    def __init__(self, group: str, protected: bool = False):
        super().__init__(protected=protected)
        self.group = group

    def compose(self):
        yield ProfileModal()
        yield Sidebar(selected_group=self.group)
        yield Header()
