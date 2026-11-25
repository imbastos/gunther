from textual.widgets import Static


class Tag(Static):
    """Etiqueta colorida para destaque de cards."""

    def __init__(self, content: str, color=None, classes: str = ""):
        super().__init__(content, classes=f"{classes} tag".strip())
        self.styles.background = color or self.app.current_theme.accent
