from textual.widgets import Button


class ActionButton(Button):
    """Botão com ação associada"""

    def __init__(self, label: str, action: callable, classes="", **kwargs):
        super().__init__(label=label, classes=classes, **kwargs)
        self._action = action

    def on_click(self):
        """Executa a ação associada ao botão"""
        if callable(self._action):
            self._action()
