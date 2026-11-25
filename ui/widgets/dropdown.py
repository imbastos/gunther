from textual.widget import Widget
from textual.widgets import Label


class Dropdown(Widget):
    """Menu suspenso genérico para ações contextuais."""

    def __init__(self, actions: dict, classes: str = ""):
        super().__init__(classes=f"bg-surface round-panel w-48 h-auto modal {classes}")
        self.actions = actions
        self.display = False

    def compose(self):
        raise NotImplementedError()

    def on_click(self, event):
        self.actions.get(event.widget.id, lambda: None)()
        self.toggle()

    def handle_signout(self):
        """Encerra a sessão atual e redireciona para a tela inicial."""
        self.screen.session_manager.end()
        self.screen.router.navigate_to("hero")
        self.app.notify("Desconectado", severity="error")

    def toggle(self, state: bool | None = None):
        if state is not None:
            self.display = state
        else:
            self.display = not self.display


class DropdownAction(Label):
    """Item de ação dentro de um Dropdown."""

    def __init__(self, id: str, text: str, caution: bool = False):
        super().__init__(
            content=text,
            id=id,
            classes=f"bg-surface p-1-2 w-full hover{' caution' if caution else ''}",
        )
