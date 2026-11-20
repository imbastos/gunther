from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from tui.widgets.alt_image import AltImage


class Sidebar(Widget):
    ITEMS = [{"label": "🏠 Página Inicial", "screen": "home", "group": "home"}]  # noqa: RUF012

    # {"home": "🏠 Página Inicial", "concepts": "📁 Conceitos"}
    def __init__(self, selected_group: str):
        super().__init__()
        self.selected_group = selected_group

    def compose(self):
        yield AltImage(image="assets/gunther.png", alt="Gunther")
        with Vertical():
            for item in self.ITEMS:
                yield SidebarItem(
                    label=item["label"],
                    target_screen=item["screen"],
                    selected=item["group"] == self.selected_group,
                )


class SidebarItem(Static):
    def __init__(self, target_screen: str, label="", selected: bool = False):
        super().__init__(
            content=label,
            classes="selected" if selected else "",
        )
        self.target_screen = target_screen

    def on_click(self):
        self.app.navigate(self.target_screen)
