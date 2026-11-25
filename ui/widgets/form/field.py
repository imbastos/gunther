from collections.abc import Iterable

from textual import on
from textual.validation import Validator
from textual.widget import Widget
from textual.widgets import Input, Label


class FormField(Widget):
    """Campo de formulário"""

    def __init__(
        self,
        placeholder: str,
        id: str,
        validators: Validator | Iterable[Validator],
        password=False,
    ):
        super().__init__(id=id, classes="w-1--1")
        self.placeholder = placeholder
        self.password = password
        self.validators = validators

    def compose(self):
        self.input = Input(
            placeholder=self.placeholder,
            validators=self.validators,
            password=self.password,
            classes="w-1--1",
        )
        self.error = Label(classes="mx-1 color-error")

        yield self.input
        yield self.error

    def is_valid(self):
        return self.input.is_valid and bool(self.input.value.strip())

    @on(Input.Changed)
    def show_invalid_reason(self, event):
        failure_descriptions = event.validation_result.failure_descriptions

        if failure_descriptions:
            error_message = (
                "* Esse campo possui " + " e ".join(failure_descriptions) + "."
            )
            self.error.update(error_message)
        else:
            self.error.update("")

    @property
    def value(self):
        return self.query_one(Input).value
