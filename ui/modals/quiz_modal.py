from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Label, RadioButton, RadioSet

from core.models import Article
from ui.widgets.action_button import ActionButton


class QuizModal(ModalScreen[bool]):
    """Modal de quiz obrigatório para concluir um conceito."""

    def __init__(self, article: Article):
        super().__init__()
        self.article = article

    def compose(self):
        with (
            Container(classes="center-container"),
            Vertical(
                id="quiz-dialog",
                classes="m-1-10-2-10 w-full bg-surface round-panel p-1-2 h-auto",
            ),
        ):
            yield Label(
                f"Quiz: {self.article.name}",
                classes="text-bold color-primary mb-1",
            )
            yield Label(
                "Responda corretamente todas as perguntas para concluir este conceito.",
                classes="color-muted mb-1",
            )

            with VerticalScroll(classes="w-full h-10 mb-1"):
                for idx, item in enumerate(self.article.questions):
                    question_text = item.get("question", f"Pergunta {idx + 1}")
                    options = item.get("options", [])
                    yield Label(
                        f"{idx + 1}. {question_text}",
                        classes="text-bold mb-1 w-full",
                    )
                    with RadioSet(id=f"quiz-question-{idx}", classes="w-full mb-1"):
                        for opt in options:
                            yield RadioButton(str(opt), classes="w-full text-wrap")

            yield Label("", id="quiz-feedback", classes="color-error mb-1")
            with Horizontal(classes="w-full h-auto"):
                yield ActionButton(
                    "Enviar respostas",
                    action=self._submit_answers,
                    id="quiz-submit-btn",
                    variant="primary",
                    classes="h-3 p-0-2 mr-1 hover-tint-white",
                )
                yield ActionButton(
                    "Cancelar",
                    action=lambda: self.dismiss(False),
                    id="quiz-cancel-btn",
                    variant="primary",
                    classes="h-3 border-none bg-panel p-0-2",
                )

    def _submit_answers(self) -> None:
        questions = self.article.questions
        correct = 0
        for idx, item in enumerate(questions):
            radio_set = self.query_one(f"#quiz-question-{idx}", RadioSet)
            if radio_set.pressed_index < 0:
                self.query_one("#quiz-feedback", Label).update(
                    "Responda todas as perguntas antes de enviar."
                )
                return
            if radio_set.pressed_index == int(item.get("correct_answer", 0)):
                correct += 1

        if correct == len(questions):
            self.dismiss(True)
        else:
            self.query_one("#quiz-feedback", Label).update(
                f"Você acertou {correct} de {len(questions)}. Tente novamente!"
            )
