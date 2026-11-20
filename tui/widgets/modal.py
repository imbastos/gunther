from textual.widget import Widget


class Modal(Widget):
    def __init__(self, actions: list):
        super().__init__()
        self.actions = actions
    
    def compose(self):
        raise NotImplementedError()

    def on_click(self, event):
        self.actions.get(event.widget.id, lambda: None)()
        self.toggle()

    def handle_signout(self):
        self.app.signout()
        self.app.notify("Desconectado", severity="error")

    def toggle(self, state: bool | None = None):
        if state is not None:
            self.display = state
        else:
            self.display = not self.display
