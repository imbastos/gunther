import webbrowser

from textual.containers import Container
from textual.widgets import Static

import config
import utils
from ui.base.screen import BaseScreen
from ui.widgets import ActionButton


class HeroScreen(BaseScreen):
    """Tela inicial do aplicativo"""

    def compose(self):
        title = Static(
            utils.title("Gunther"),
            classes="text-bold color-primary text-center mb-1",
        )
        slogan = Static(
            "Aprenda a arquitetura que move a tecnologia",
            classes="text-italic color-muted text-center mb-2",
        )
        connect = ActionButton(
            "▶ Conectar",
            classes="mx-1 w-1--1",
            action=lambda: self.router.navigate_to(screen="auth"),
            variant="primary",
        )
        github = ActionButton(
            "😸 Repositório", classes="mx-1 w-1--1", action=self.handle_github
        )

        with (
            Container(classes="center-container"),
            Container(classes="content-container w-1--3"),
        ):
            yield title
            yield slogan

            with Container(classes="horizontal content-alignment"):
                yield connect
                yield github

    def handle_github(self):
        webbrowser.open_new_tab(url=config.REPOSITORY_URL)
        self.app.notify("Nova aba aberta")
