from uuid import UUID

from textual.containers import Container, Grid, Horizontal, Vertical
from textual.widgets import Input, Label, Static

from core.exceptions.user import UserError
from core.models import Article, User
from ui.modals.file_picker import FilePickerModal
from ui.templates import Shell
from ui.utils import copy_user_photo
from ui.widgets.action_button import ActionButton
from ui.widgets.alt_image import AltImage


class ProfileScreen(Shell):
    """Tela de perfil dinâmica para exibir os dados reais de um usuário."""

    group = "profile"

    def __init__(self, user_id: UUID | str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.target_user_id = user_id

    def _get_completed_articles(self, user: User | None) -> list[Article]:
        if user is None or self.article_service is None:
            return []
        completed_ids = {str(cid) for cid in user.completed_concepts}
        return [
            article
            for article in self.article_service.get_all()
            if str(article.id) in completed_ids
        ]

    def _get_authored_articles(self, user: User | None) -> list[Article]:
        if user is None or self.article_service is None:
            return []
        user_id_str = str(user.id)
        return [
            article
            for article in self.article_service.get_all()
            if str(article.author) == user_id_str
        ]

    def __get_user(self):
        target_id = self.target_user_id
        if target_id is None:
            return self.current_user
        try:
            return self.user_service.get_by_id(user_id=target_id)
        except UserError as e:
            self.app.notify(e.message, severity="error")
            return None

    def _is_own_profile(self, user: User | None) -> bool:
        me = self.current_user
        return me is not None and user is not None and str(me.id) == str(user.id)

    def compose(self):
        user = self.__get_user()
        completed_articles = self._get_completed_articles(user)
        authored_articles = self._get_authored_articles(user)

        yield from super().compose()
        with Container(classes="main"):
            if user is None:
                yield Label("Usuário não encontrado", classes="text-bold color-error")
                return

            with Vertical(classes="w-full h-auto center mb-1"):
                with Container(classes="w-full h-auto center"):
                    yield AltImage(
                        image=user.image or "assets/icon.png",
                        alt="👤",
                        classes="square-8 bg-surface mb-1",
                    )

                yield Label(
                    f"{user.name}{' 👾' if user.role == 'admin' else ''}",
                    id="profile-name",
                    classes="text-center w-full text-bold",
                )
                yield Label(
                    f"@{user.username}",
                    id="profile-username",
                    classes="text-center w-full color-muted",
                )

            with (
                Container(classes="w-full h-auto center mb-2"),
                Grid(classes="w-1--3 gutter-1 cols-2 bg-surface p-1-2 center"),
            ):
                with Vertical(classes="center text-center"):
                    yield Label(
                        str(len(completed_articles)),
                        id="profile-completed-count",
                        classes="w-1--1 text-center",
                    )
                    yield Label("Concluídos", classes="w-1--1 color-muted text-center")
                with Vertical(classes="center"):
                    yield Label(
                        str(len(authored_articles)),
                        id="profile-authored-count",
                        classes="w-1--1 text-center",
                    )
                    yield Label("Criados", classes="w-1--1 color-muted text-center")

            with Vertical(classes="w-full h-auto mb-2"):
                yield Label(
                    "[📚] Conceitos",
                    classes="color-muted mb-1",
                )
                if completed_articles:
                    with Grid(classes="w-full h-auto cols-3 gutter-1"):
                        for concept in completed_articles:
                            yield _CompletedConceptCard(concept)
                else:
                    yield Label(
                        "Nenhum conceito concluído ainda.",
                        classes="color-muted",
                    )

            with Vertical(classes="w-full h-auto mb-2"):
                yield Label(
                    "[👤] Dados",
                    classes="color-muted mb-1",
                )
                with Vertical(classes="w-full h-auto bg-panel border-l-primary p-1-2"):
                    yield Label(
                        f"Membro desde: {user.created_at}",
                        id="profile-created-at",
                        classes="color-muted",
                    )

            if self._is_own_profile(user):
                with Vertical(
                    id="profile-edit-section",
                    classes="w-full h-auto mb-2",
                ):
                    yield Label(
                        "[✏️] Editar perfil",
                        classes="color-muted mb-1",
                    )
                    with Vertical(classes="w-full h-auto bg-panel border-l-surface p-1-2"):
                        yield Input(
                            value=user.name,
                            placeholder="Seu nome",
                            id="profile-edit-name-input",
                            classes="w-full mb-1",
                        )
                        with Horizontal(classes="w-full h-auto mb-1"):
                            yield Input(
                                value="",
                                placeholder="Caminho da foto no computador (opcional)",
                                id="profile-edit-photo-input",
                                classes="w-1--1 mr-1",
                            )
                            yield ActionButton(
                                "Procurar...",
                                action=lambda: self.app.push_screen(
                                    FilePickerModal(),
                                    callback=self._on_photo_picked,
                                ),
                                id="profile-pick-photo-btn",
                                classes="h-3 border-none bg-surface p-0-2 hover-tint-white",
                            )
                        yield ActionButton(
                            "Salvar alterações",
                            action=self._save_profile,
                            id="profile-save-btn",
                            classes="h-3 border-none bg-success p-0-2 hover-tint-white",
                        )

    def _on_photo_picked(self, path: str | None) -> None:
        if path:
            self.query_one("#profile-edit-photo-input", Input).value = path

    def _save_profile(self) -> None:
        user = self.current_user
        if user is None:
            self.app.notify("Usuário não autenticado.", severity="error")
            return

        name = self.query_one("#profile-edit-name-input", Input).value.strip()
        photo_path = self.query_one("#profile-edit-photo-input", Input).value.strip()

        if not name:
            self.app.notify("O nome não pode ficar vazio.", severity="error")
            return

        if photo_path:
            try:
                user.image = copy_user_photo(photo_path, user.id)
            except FileNotFoundError:
                self.app.notify("Arquivo de foto não encontrado.", severity="error")
                return

        user.name = name
        self.user_service.update(user)
        self.app.notify("Perfil atualizado com sucesso!")
        self.router.navigate_to("profile", user_id=user.id)


class _CompletedConceptCard(Static):
    """Card clicável de conceito concluído no perfil."""

    def __init__(self, concept: Article):
        super().__init__(
            content=f"✅ {concept.name}\n[$foreground-muted]{concept.description[:48]}",
            id=f"profile-completed-{concept.id}",
            classes="w-full h-auto p-1-2 bg-surface hover border-l-success",
        )
        self.concept = concept

    def on_click(self) -> None:
        self.screen.router.navigate_to("concept", article_id=self.concept.id)
