from textual.widgets import DataTable

from ui.base.screen import BaseScreen
from ui.widgets.action_button import ActionButton


class UserListScreen(BaseScreen):
    """Tela para exibir a lista de usuários"""

    def __init__(self):
        super().__init__()
        self.users = self.user_service.get_all()

    def compose(self):
        yield DataTable(id="user_table")

        yield ActionButton("◀ Voltar", action=self.handle_hero, variant="primary")

    def handle_hero(self):
        self.app.navigate_to(screen="hero")

    def on_mount(self):
        user_table = self.query_one("#user_table", DataTable)
        user_table.add_columns("ID", "Name", "Email", "Created At")
        for user in self.users:
            user_table.add_row(
                str(user.id), user.name, user.email, str(user.created_at)
            )
