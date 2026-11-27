from uuid import UUID

from textual.containers import Vertical
from textual.widgets import Label

from core.exceptions.game import NotFoundGameError
from core.models import Game
from ui.screens.game import GameScreen


class ChallengeScreen(GameScreen):
    """Tela de execução de um desafio ArchKata com diagrama e dados do desafio."""

    def __init__(
        self,
        game_id: UUID | str | None = None,
        game: Game | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.challenge = self._resolve_game(game, game_id)

    def _resolve_game(
        self, game: Game | None, game_id: UUID | str | None
    ) -> Game | None:
        if game is not None:
            return game
        if game_id is not None and self.game_service is not None:
            try:
                return self.game_service.get_by_id(game_id)
            except NotFoundGameError:
                return None
        return None

    def compose(self):
        yield from super().compose()
        # if self.challenge is None:
        #     with Vertical(
        #         classes="absolute o-2 p-1 round-surface bg-surface w-auto"
        #     ):
        #         yield Label("Desafio não encontrado.", classes="color-error")
        #     return

        # dots = "●" * (self.challenge.difficulty or 1)
        # with Vertical(
        #     id="challenge-info",
        #     classes="absolute o-2 p-1 round-surface bg-surface w-auto",
        # ):
        #     yield Label(
        #         self.challenge.name,
        #         id="challenge-name",
        #         classes="text-bold color-primary mb-1",
        #     )
        #     with Vertical(classes="w-32"):
        #         if self.challenge.description:
        #             yield Label(
        #                 f"[$primary]•[$foreground-muted] {self.challenge.description}",
        #                 id="challenge-description",
        #                 classes="w-full mb-1",
        #             )
        #         yield Label(
        #             f"Dificuldade: {dots} • {self.challenge.xp} XP",
        #             id="challenge-meta",
        #             classes="color-accent w-full",
        #         )
