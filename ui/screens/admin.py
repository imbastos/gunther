import re
from uuid import UUID

from textual.containers import Container, Grid, Horizontal, Vertical
from textual.widgets import (
    DataTable,
    Input,
    Label,
    Select,
    Switch,
    TabbedContent,
    TabPane,
    TextArea,
)

from core.exceptions.article import DuplicateArticleSlugError
from core.models import Article, ArticleArea, Post
from ui.templates import Shell
from ui.widgets.action_button import ActionButton


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower().strip())
    return slug.strip("-") or "conceito"


class AdminScreen(Shell):
    """Painel administrativo visível apenas para usuários com role admin."""

    group = "admin"

    def __init__(self, active_tab: str = "tab-posts", **kwargs):
        super().__init__(**kwargs)
        self.active_tab = active_tab

    def _reload(self, active_tab: str) -> None:
        self.router.navigate_to("admin", active_tab=active_tab)

    def _set_highlighted_post(self, target_id: UUID | str) -> None:
        if self.post_service is None:
            return
        target_str = str(target_id)
        for post in self.post_service.get_all():
            should_highlight = str(post.id) == target_str
            if post.is_highlighted != should_highlight:
                post.is_highlighted = should_highlight
                self.post_service.update(post)

    def compose(self):
        yield from super().compose()

        with Container(classes="main"):
            if not self.is_admin:
                with Vertical(
                    classes="w-full h-auto bg-panel border-l-accent p-1-2 mb-1"
                ):
                    yield Label(
                        "Acesso negado",
                        id="admin-access-denied",
                        classes="text-bold color-error mb-1",
                    )
                    yield Label(
                        "Esta área é restrita a usuários administradores.",
                        classes="color-muted",
                    )
                return

            posts = self.post_service.get_all() if self.post_service else []
            articles = self.article_service.get_all() if self.article_service else []
            users = self.user_service.get_all() if self.user_service else []
            admin_count = sum(1 for u in users if u.role == "admin")

            yield Label(
                "🔨 Painel Administrativo", classes="text-bold color-primary mb-1"
            )

            with Grid(classes="w-full h-auto cols-3 gutter-1 mb-2"):
                with Vertical(classes="bg-surface p-1-2 border-l-primary w-full"):
                    yield Label(
                        str(len(posts)), id="admin-stat-posts", classes="text-bold"
                    )
                    yield Label("Artigos", classes="color-muted")
                with Vertical(classes="bg-surface p-1-2 border-l-success w-full"):
                    yield Label(
                        str(len(articles)),
                        id="admin-stat-concepts",
                        classes="text-bold",
                    )
                    yield Label("Conceitos", classes="color-muted")
                with Vertical(classes="bg-surface p-1-2 border-l-accent w-full"):
                    yield Label(
                        f"{len(users)} ({admin_count} admin)",
                        id="admin-stat-users",
                        classes="text-bold",
                    )
                    yield Label("Usuários", classes="color-muted")

            with TabbedContent(
                initial=self.active_tab, id="admin-tabs", classes="w-full h-auto"
            ):
                with TabPane("Artigos", classes="w-1--1", id="tab-posts"):
                    yield from self._compose_posts_tab(posts)
                with TabPane("Conceitos", classes="w-1--1", id="tab-concepts"):
                    yield from self._compose_concepts_tab(articles)
                with TabPane("Usuários", classes="w-1--1", id="tab-users"):
                    yield from self._compose_users_tab(users)

    def _compose_posts_tab(self, posts: list[Post]):
        yield Label("[ 📝 ] Criar Novo Artigo", classes="color-muted mb-1 mt-1")
        with Vertical(classes="w-full h-auto bg-panel border-l-primary p-1-2 mb-2"):
            yield Input(
                placeholder="Título do artigo",
                id="post-name-input",
                classes="w-full mb-1",
            )
            yield Input(
                placeholder="Imagem de capa (caminho ou URL, opcional)",
                id="post-image-input",
                classes="w-full mb-1",
            )
            yield Label("Conteúdo (Markdown):", classes="color-muted mb-1")
            yield TextArea(id="post-text-input", classes="w-full h-8 mb-1 bg-surface")
            with Horizontal(classes="w-full h-auto mb-1"):
                yield Switch(value=False, id="post-highlighted-switch")
                yield Label(
                    "Definir como artigo em destaque", classes="ml-2 content-center"
                )
            yield ActionButton(
                "Criar Artigo",
                action=self._handle_create_post,
                id="create-post-btn",
                classes="h-3 border-none bg-success p-0-2 hover-tint-white",
            )

        yield Label("[ ⭐ ] Artigos Cadastrados", classes="color-muted mb-1")
        if not posts:
            yield Label("Nenhum artigo cadastrado.", classes="color-muted mb-2")
            return

        for post in posts:
            border = "border-l-accent" if post.is_highlighted else "border-l-surface"
            with Horizontal(classes=f"w-full h-auto bg-surface {border} p-1-2 mb-1"):
                with Vertical(classes="w-1--1 h-auto"):
                    badge = " ⭐ EM DESTAQUE" if post.is_highlighted else ""
                    yield Label(f"{post.name}{badge}", classes="text-bold w-full")
                    yield Label(
                        f"Criado em: {post.created_at}",
                        classes="color-muted w-full",
                    )
                if post.is_highlighted:
                    yield ActionButton(
                        "Remover destaque",
                        action=lambda pid=post.id: self._handle_unhighlight_post(pid),
                        id=f"unhighlight-post-{post.id}",
                        classes="h-3 border-none bg-panel p-0-2 mr-1 hover-tint-white",
                    )
                else:
                    yield ActionButton(
                        "Destacar",
                        action=lambda pid=post.id: self._handle_highlight_post(pid),
                        id=f"highlight-post-{post.id}",
                        classes="h-3 border-none bg-panel p-0-2 mr-1 hover-tint-white",
                    )
                yield ActionButton(
                    "Excluir",
                    action=lambda pid=post.id: self._handle_delete_post(pid),
                    id=f"delete-post-{post.id}",
                    classes="h-3 border-none bg-panel p-0-2 caution hover",
                )

    def _compose_concepts_tab(self, articles: list[Article]):
        area_options = [
            (area.value.replace("_", " ").title(), area.value) for area in ArticleArea
        ]
        parent_options: list[tuple[str, str | None]] = [
            ("Raiz (sem conceito pai)", None)
        ]
        parent_options.extend((article.name, str(article.id)) for article in articles)

        yield Label("[ 📚 ] Criar Novo Conceito", classes="color-muted mb-1 mt-1")
        with Vertical(classes="w-full h-auto bg-panel border-l-success p-1-2 mb-2"):
            yield Input(
                placeholder="Nome do conceito",
                id="concept-name-input",
                classes="w-full mb-1",
            )
            yield Input(
                placeholder="Slug (opcional, gerado automaticamente se vazio)",
                id="concept-slug-input",
                classes="w-full mb-1",
            )
            yield Input(
                placeholder="Descrição breve",
                id="concept-desc-input",
                classes="w-full mb-1",
            )
            with Grid(classes="w-full h-auto cols-3 gutter-1 mb-1"):
                yield Select(
                    options=area_options,
                    value=ArticleArea.REQUISITOS.value,
                    allow_blank=False,
                    id="concept-area-select",
                    classes="w-full",
                )
                yield Select(
                    options=parent_options,
                    value=None,
                    allow_blank=False,
                    id="concept-parent-select",
                    classes="w-full",
                )
                yield Input(
                    placeholder="Ordem (0)",
                    value="0",
                    id="concept-order-input",
                    classes="w-full",
                )
            yield Label("Introdução:", classes="color-muted mb-1")
            yield TextArea(
                id="concept-intro-input", classes="w-full h-6 mb-1 bg-surface"
            )
            yield Label("Explicação:", classes="color-muted mb-1")
            yield TextArea(
                id="concept-expl-input", classes="w-full h-8 mb-1 bg-surface"
            )
            yield Label(
                "Perguntas do Quiz (opcional: uma por linha 'Pergunta | Op1; Op2 | índice_correto'):",
                classes="color-muted mb-1",
            )
            yield TextArea(
                id="concept-questions-input", classes="w-full h-6 mb-1 bg-surface"
            )
            yield Input(
                placeholder="Imagem ilustrativa (opcional)",
                id="concept-image-input",
                classes="w-full mb-1",
            )
            with Horizontal(classes="w-full h-auto mb-1"):
                yield Switch(value=True, id="concept-published-switch")
                yield Label("Publicado para estudantes", classes="ml-2 content-center")
            yield ActionButton(
                "Criar Conceito",
                action=self._handle_create_concept,
                id="create-concept-btn",
                classes="h-3 border-none bg-success p-0-2 hover-tint-white",
            )

        yield Label("[ 🗂 ] Conceitos Cadastrados", classes="color-muted mb-1")
        if not articles:
            yield Label("Nenhum conceito cadastrado.", classes="color-muted mb-2")
            return

        for article in articles:
            status = "Publicado" if article.is_published else "Rascunho"
            border = "border-l-success" if article.is_published else "border-l-surface"
            with Horizontal(classes=f"w-full h-auto bg-surface {border} p-1-2 mb-1"):
                with Vertical(classes="w-1--1 h-auto"):
                    yield Label(
                        f"{article.name} ({status})", classes="text-bold w-full"
                    )
                    yield Label(
                        f"Slug: {article.slug} • Área: {article.area}",
                        classes="color-muted w-full",
                    )
                toggle_label = "Despublicar" if article.is_published else "Publicar"
                yield ActionButton(
                    toggle_label,
                    action=lambda cid=article.id: self._handle_toggle_publish_concept(
                        cid
                    ),
                    id=f"toggle-publish-concept-{article.id}",
                    classes="h-3 border-none bg-panel p-0-2 mr-1 hover-tint-white",
                )
                yield ActionButton(
                    "Excluir",
                    action=lambda cid=article.id: self._handle_delete_concept(cid),
                    id=f"delete-concept-{article.id}",
                    classes="h-3 border-none bg-panel p-0-2 caution hover",
                )

    def _compose_users_tab(self, users: list):
        yield Label("[ 👥 ] Usuários Cadastrados", classes="color-muted mb-1 mt-1")
        yield DataTable(id="admin-users-table", classes="w-full h-10 mb-2 bg-surface")

        for user in users:
            border = "border-l-primary" if user.role == "admin" else "border-l-surface"
            with Horizontal(classes=f"w-full h-auto bg-surface {border} p-1-2 mb-1"):
                with Vertical(classes="w-1--1 h-auto"):
                    yield Label(
                        f"{user.name} (@{user.username}) [{user.role}]",
                        classes="text-bold w-full",
                    )
                    yield Label(
                        f"{user.email} • Concluídos: {len(user.completed_concepts)}",
                        classes="color-muted w-full",
                    )
                yield ActionButton(
                    "Perfil",
                    action=lambda uid=user.id: self.router.navigate_to(
                        "profile", user_id=uid
                    ),
                    id=f"view-user-{user.id}",
                    classes="h-3 border-none bg-panel p-0-2 mr-1 hover-tint-white",
                )
                next_role = "user" if user.role == "admin" else "admin"
                yield ActionButton(
                    f"Tornar {next_role}",
                    action=lambda uid=user.id: self._handle_toggle_user_role(uid),
                    id=f"toggle-role-user-{user.id}",
                    classes="h-3 border-none bg-panel p-0-2 hover-tint-white",
                )

    def on_mount(self) -> None:
        if not self.is_admin:
            return
        table = self.query_one("#admin-users-table", DataTable)
        table.add_columns(
            "Nome", "Username", "Email", "Role", "Concluídos", "Criado em"
        )
        users = self.user_service.get_all() if self.user_service else []
        for user in users:
            table.add_row(
                user.name,
                f"@{user.username}",
                user.email,
                user.role,
                str(len(user.completed_concepts)),
                str(user.created_at),
            )

    def _handle_highlight_post(self, post_id: UUID | str) -> None:
        if not self.is_admin:
            return
        self._set_highlighted_post(post_id)
        self.app.notify("Artigo em destaque atualizado!")
        self._reload("tab-posts")

    def _handle_unhighlight_post(self, post_id: UUID | str) -> None:
        if not self.is_admin or self.post_service is None:
            return
        post = self.post_service.get_by_id(post_id)
        post.is_highlighted = False
        self.post_service.update(post)
        self.app.notify("Destaque removido do artigo.")
        self._reload("tab-posts")

    def _handle_delete_post(self, post_id: UUID | str) -> None:
        if not self.is_admin or self.post_service is None:
            return
        self.post_service.delete(post_id)
        self.app.notify("Artigo excluído.")
        self._reload("tab-posts")

    def _handle_toggle_publish_concept(self, concept_id: UUID | str) -> None:
        if not self.is_admin or self.article_service is None:
            return
        concept = self.article_service.get_by_id(concept_id)
        if concept.is_published:
            self.article_service.unpublish(concept_id)
            self.app.notify("Conceito movido para rascunho.")
        else:
            self.article_service.publish(concept_id)
            self.app.notify("Conceito publicado!")
        self._reload("tab-concepts")

    def _handle_delete_concept(self, concept_id: UUID | str) -> None:
        if not self.is_admin or self.article_service is None:
            return
        self.article_service.delete(concept_id)
        self.app.notify("Conceito excluído.")
        self._reload("tab-concepts")

    def _handle_create_post(self) -> None:
        if self.post_service is None:
            return
        name = self.query_one("#post-name-input", Input).value.strip()
        image = self.query_one("#post-image-input", Input).value.strip() or None
        text = self.query_one("#post-text-input", TextArea).text.strip()
        is_highlighted = self.query_one("#post-highlighted-switch", Switch).value

        if not name or not text:
            self.app.notify("Informe título e conteúdo do artigo.", severity="error")
            return

        post = self.post_service.create(
            Post(
                name=name,
                text=text,
                image=image,
                is_highlighted=is_highlighted,
            )
        )
        if is_highlighted:
            self._set_highlighted_post(post.id)

        self.app.notify("Artigo criado com sucesso!")
        self._reload("tab-posts")

    def _handle_create_concept(self) -> None:
        if self.article_service is None:
            return
        name = self.query_one("#concept-name-input", Input).value.strip()
        raw_slug = self.query_one("#concept-slug-input", Input).value.strip()
        description = self.query_one("#concept-desc-input", Input).value.strip()
        area = self.query_one("#concept-area-select", Select).value
        parent_raw = self.query_one("#concept-parent-select", Select).value
        order_raw = self.query_one("#concept-order-input", Input).value.strip()
        introduction = self.query_one("#concept-intro-input", TextArea).text.strip()
        explanation = self.query_one("#concept-expl-input", TextArea).text.strip()
        questions_raw = self.query_one(
            "#concept-questions-input", TextArea
        ).text.strip()
        image = self.query_one("#concept-image-input", Input).value.strip() or None
        is_published = self.query_one("#concept-published-switch", Switch).value

        if not name or not description or not introduction or not explanation:
            self.app.notify(
                "Preencha nome, descrição, introdução e explicação do conceito.",
                severity="error",
            )
            return

        questions: list[dict] = []
        if questions_raw:
            for line in questions_raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) != 3:
                    self.app.notify(
                        "Formato de pergunta inválido. Use: Pergunta | Op1; Op2 | índice",
                        severity="error",
                    )
                    return
                options = [o.strip() for o in parts[1].split(";") if o.strip()]
                try:
                    answer_idx = int(parts[2])
                except ValueError:
                    self.app.notify(
                        "Índice da resposta deve ser inteiro.", severity="error"
                    )
                    return
                questions.append(
                    {"question": parts[0], "options": options, "answer": answer_idx}
                )

        try:
            order = int(order_raw) if order_raw else 0
        except ValueError:
            self.app.notify("A ordem deve ser um número inteiro.", severity="error")
            return

        slug = raw_slug or _slugify(name)
        parent_id = (
            UUID(str(parent_raw)) if parent_raw not in (None, Select.BLANK) else None
        )
        author_id = str(self.current_user.id) if self.current_user else "admin"

        try:
            self.article_service.create(
                Article(
                    name=name,
                    slug=slug,
                    description=description,
                    area=str(area),
                    parent_id=parent_id,
                    order=order,
                    introduction=introduction,
                    explanation=explanation,
                    questions=questions,
                    image=image,
                    is_published=is_published,
                    author=author_id,
                )
            )
        except DuplicateArticleSlugError:
            self.app.notify("Já existe um conceito com este slug.", severity="error")
            return

        self.app.notify("Conceito criado com sucesso!")
        self._reload("tab-concepts")

    def _handle_toggle_user_role(self, user_id: str) -> None:
        if self.user_service is None:
            return
        user = self.user_service.get_by_id(user_id)
        if user is None:
            self.app.notify("Usuário não encontrado.", severity="error")
            return
        if self.current_user is not None and str(user.id) == str(self.current_user.id):
            self.app.notify(
                "Não é possível alterar sua própria função de administrador.",
                severity="warning",
            )
            return

        user.role = "user" if user.role == "admin" else "admin"
        self.user_service.update(user)
        self.app.notify(f"Função de {user.name} alterada para {user.role}.")
        self._reload("tab-users")
