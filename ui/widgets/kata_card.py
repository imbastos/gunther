from textual.color import Color
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Label

from core.models import Game
from ui.widgets.tag import Tag


class KataCard(Widget):
    """Card clicável para exibir um desafio ArchKata."""

    def __init__(
        self,
        game: Game,
        weekly: bool = False,
        classes: str = "",
    ):
        super().__init__(classes=f"w-full h-auto {classes}".strip())
        self.game = game
        self.weekly = weekly

    def compose(self):
        border = "border-l-accent" if self.weekly else "border-l-primary"
        with Vertical(classes=f"p-1-2 bg-surface hover {border} w-full h-auto"):
            if self.weekly:
                yield Tag(
                    "🎯 Desafio Semanal",
                    color=Color.parse(self.app.current_theme.accent).with_alpha(0.2),
                    classes="mb-1",
                )

            yield Label(self.game.name, classes="text-bold mb-1 w-full")
            if self.game.description:
                limit = 120 if self.game.is_weekly else 40
                description = self.game.description[:limit]

                if len(self.game.description) > limit:
                    description += "..."

                yield Label(description, classes="color-muted w-full mb-1")

            dots = "●" * (self.game.difficulty or 1)
            yield Label(
                f"Dificuldade: {dots} • {self.game.xp} XP",
                classes="color-accent w-full",
            )

    def on_click(self) -> None:
        from ui.modals.kata_modal import KataModal

        self.app.push_screen(
            KataModal(self.game),
            callback=self._on_modal_result,
        )

    def _on_modal_result(self, start: bool) -> None:
        if start:
            self.screen.router.navigate_to("challenge", game_id=self.game.id)
