from textual.containers import Container, Grid, Vertical
from textual.widgets import Label

from ui.templates import Shell
from ui.widgets.kata_card import KataCard


class ArchKataScreen(Shell):
    """Tela principal do ArchKata com desafio semanal e lista de katas."""

    group = "archkata"

    def compose(self):
        weekly = self.game_service.get_weekly() if self.game_service else None
        games = self.game_service.get_all() if self.game_service else []
        other_games = [
            g for g in games if weekly is None or str(g.id) != str(weekly.id)
        ]

        yield from super().compose()
        with Container(classes="main"):
            if weekly is not None:
                with Vertical(classes="w-full h-auto mb-2"):
                    yield Label("[🎯] Desafio Semanal", classes="color-muted mb-1")
                    yield KataCard(game=weekly, weekly=True)

            with Vertical(classes="w-full h-auto mb-2"):
                yield Label("[🧩] Katas", classes="color-muted mb-1")
                if other_games:
                    with Grid(classes="w-full h-auto cols-3 gutter-1"):
                        for game in other_games:
                            yield KataCard(game=game)
                elif weekly is None:
                    yield Label("Nenhum kata cadastrado.", classes="color-muted")
