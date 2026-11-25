import os
from uuid import UUID

from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static

from core.exceptions.article import NotFoundArticleError
from core.models import Article
from ui.modals.quiz_modal import QuizModal
from ui.templates import Shell
from ui.widgets import ActionButton, AltImage
from ui.widgets.concept.article_section import ArticleSection
from ui.widgets.concept.formatter import format_collection_items
from ui.widgets.header.streak import Streak


class ConceptScreen(Shell):
    """Tela de exibição de um conceito/artigo."""

    group = "concept"

    def __init__(
        self,
        article_id: UUID | str | None = None,
        slug: str | None = None,
        **kwargs,
    ):
        super().__init__(
            selected_article_id=article_id,
            concepts_expanded=True,
            **kwargs,
        )

        self._requested_id = article_id
        self._requested_slug = slug
        self.article = self._resolve_article()

        if self.article:
            self.selected_article_id = self.article.id

        self.parent_article = self._resolve_parent()
        self.child_articles = self._resolve_children()

    def _resolve_article(self) -> Article | None:
        if self.article_service is None:
            return None

        try:
            if self._requested_id is not None:
                return self.article_service.get_by_id(self._requested_id)

            if self._requested_slug is not None:
                return self.article_service.find_by_slug(self._requested_slug)

        except NotFoundArticleError:
            return None

        articles = self.article_service.get_all()
        return articles[0] if articles else None

    def _resolve_parent(self) -> Article | None:
        if not self.article or not self.article.parent_id:
            return None

        try:
            return self.article_service.get_by_id(self.article.parent_id)
        except NotFoundArticleError:
            return None

    def _resolve_children(self) -> list[Article]:
        if not self.article or self.article_service is None:
            return []

        return self.article_service.get_children(self.article.id)

    def _is_completed(self) -> bool:
        user = self.current_user
        return bool(
            self.article and user and str(self.article.id) in user.completed_concepts
        )

    def _section(self, title: str, content: str, border: str, widget_id: str):
        yield Static(title, classes="color-muted mb-1")

        with Vertical(classes=f"w-full h-auto bg-panel {border} p-1-2 mb-2"):
            yield Static(content, id=widget_id)

    def _set_completion_state(self, completed: bool) -> None:
        button = self.query_one("#concept-complete-btn", Button)
        button.label = "✓ Concluído" if completed else "✓ Marcar como concluído"

        button.remove_class("bg-surface", "bg-success")
        button.add_class("bg-success" if completed else "bg-surface")

    def compose(self):
        if not self.article:
            with Vertical(classes="w-full h-auto bg-panel border-l-surface p-1-2 mb-1"):
                yield Static(
                    "Conceito não encontrado",
                    classes="text-bold color-primary mb-1",
                )
                yield Static(
                    "Selecione um conceito na barra lateral ou cadastre um novo artigo.",
                    classes="color-muted",
                )
            return

        article = self.article
        area = getattr(article.area, "value", article.area)
        status = "Publicado" if article.is_published else "Rascunho"
        border = "border-l-success" if article.is_published else "border-l-accent"

        if self.parent_article:
            parent_id = self.parent_article.id
            yield ActionButton(
                f"◀ Voltar para: {self.parent_article.name}",
                action=lambda pid=parent_id: self.router.navigate_to(
                    "concept", article_id=pid
                ),
                id="concept-parent-btn",
                classes="h-3 border-none bg-surface p-0-2 mb-1 hover-tint-white",
            )

        yield Static("[ 📖 ] Conceito", classes="color-muted mb-1")

        with Vertical(classes=f"w-full h-auto bg-panel {border} p-1-2 mb-2"):
            yield Static(
                article.name,
                id="concept-name",
                classes="text-bold color-primary mb-1",
            )

            with Horizontal(classes="w-full h-auto mb-1"):
                for label, value in (
                    ("Área", area),
                    ("Slug", f"/{article.slug}"),
                    ("Status", status),
                    ("Ordem", article.order),
                ):
                    yield Static(
                        f"{label}: {value}",
                        classes="color-muted mr-2",
                    )

            yield Static(article.description, id="concept-description")

            if article.image:
                if os.path.isfile(article.image):
                    yield AltImage(
                        image=article.image,
                        alt=f"🖼 {article.image}",
                    )
                else:
                    yield Static(
                        f"🖼 Imagem: {article.image}",
                        id="concept-image",
                        classes="color-muted mt-1",
                    )

        yield ArticleSection(
            "[ 📝 ] Introdução",
            article.introduction,
            widget_id="concept-introduction",
        )

        yield ArticleSection(
            "[ 💡 ] Explicação",
            article.explanation,
            widget_id="concept-explanation",
        )

        yield ArticleSection(
            "[ 🧪 ] Exemplos",
            format_collection_items(
                article.examples,
                "Nenhum exemplo cadastrado.",
            ),
            border="border-l-success",
            widget_id="concept-examples",
        )

        yield ArticleSection(
            "[ 🔗 ] Referências",
            format_collection_items(
                article.references,
                "Nenhuma referência cadastrada.",
            ),
            border="border-l-surface",
            widget_id="concept-references",
        )

        if self.child_articles:
            yield Static("[ 🗂️ ] Subconceitos", classes="color-muted mb-1")

            with (
                Vertical(classes="w-full h-auto bg-panel border-l-surface p-1-2 mb-2"),
                Horizontal(classes="w-full h-auto"),
            ):
                for child in self.child_articles:
                    yield ActionButton(
                        child.name,
                        action=lambda cid=child.id: self.router.navigate_to(
                            "concept", article_id=cid
                        ),
                        id=f"concept-child-{child.id}",
                        classes="h-3 border-none bg-surface p-0-2 mr-1 mb-1 hover-tint-white",
                    )

        completed = self._is_completed()

        yield ActionButton(
            "✓ Concluído" if completed else "✓ Marcar como concluído",
            action=self._handle_complete_toggle,
            id="concept-complete-btn",
            classes=(
                "h-3 border-none "
                f"{'bg-success' if completed else 'bg-surface'} "
                "p-0-2 mb-2 hover-tint-white"
            ),
        )

    def _handle_complete_toggle(self) -> None:
        if not self.article:
            return
        session = self.session_manager.current_session

        if session is None or self.user_service is None:
            self.app.notify("Usuário não autenticado.", severity="error")
            return

        if self._is_completed():
            self.user_service.uncomplete_concept(
                session.user_id,
                self.article.id,
            )
            self._set_completion_state(False)
            self.app.notify("Conclusão removida do conceito.")

        elif self.article.questions:
            self.app.push_screen(
                QuizModal(self.article),
                callback=self._on_quiz_finished,
            )

        else:
            self._complete_current_concept()

    def _on_quiz_finished(self, passed: bool) -> None:
        if passed:
            self._complete_current_concept()

    def _complete_current_concept(self) -> None:
        session = self.session_manager.current_session

        if not session or not self.user_service or not self.article:
            return

        self.user_service.complete_concept(session.user_id, self.article.id)
        self._set_completion_state(True)

        for streak in self.query(Streak):
            streak.refresh_streak()

        self.app.notify("Conceito marcado como concluído!")
