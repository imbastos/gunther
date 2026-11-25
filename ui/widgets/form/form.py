from textual import on
from textual.widget import Widget
from textual.widgets import Input

from ui.widgets.action_button import ActionButton
from ui.widgets.form.field import FormField


class Form(Widget):
    """Formulário"""

    def __init__(
        self, fields: list[FormField], on_submit: callable, submit_message="Confirmar"
    ):
        super().__init__()
        self.fields = fields
        self.submit_message = submit_message
        self.on_submit = on_submit

    def compose(self):
        self.submit = ActionButton(
            label=self.submit_message,
            variant="primary",
            action=self.__on_submit,
            classes="w-1--1 mx-1",
        )

        yield from self.fields
        yield self.submit

    def __on_submit(self):
        self.on_submit(self.__data)

    def on_mount(self):
        self.update_submit_state()

    @on(Input.Changed)
    def on_input_changed(self):
        self.update_submit_state()

    def update_submit_state(self):
        all_valid = all(field.is_valid() for field in self.fields)

        self.submit.disabled = not all_valid

    @property
    def __data(self):
        values = {}
        for field in self.fields:
            values[field.id] = field.value
        return values
