from textual.widgets import Static


class SidebarItem(Static):
    """Item de navegação principal."""

    def __init__(
        self,
        target_screen: str,
        label: str = "",
        selected: bool = False,
        **kwargs,
    ):
        classes = (
            "w-full bg-background border-none mb-1 p-1-2 text-left hover-tint-white"
        )

        if selected:
            classes += " tint-white-5 text-bold"

        super().__init__(label, classes=classes, **kwargs)
        self.target_screen = target_screen

    def on_click(self) -> None:
        self.screen.router.navigate_to(self.target_screen)
