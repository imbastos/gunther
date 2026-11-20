from textual import on
from textual.widget import Widget
from textual.widgets import Button, Input

from tui.widgets.form_field import FormField


class Form(Widget):
    def __init__(self):
        super().__init__()

    @on(Input.Changed)
    def on_change(self):
        self.__update_submit_state()

    @on(Input.Submitted)
    def handle_enter(self):
        self.handle_submit()

    @on(Button.Pressed, ".submit")
    def handle_submit(self):
        if not self.__is_form_filled():
            return
        self.__update_fields_state(False)
        self.on_submit()
        self.__update_fields_state(True)

    def on_mount(self):
        self.__update_submit_state()

    def on_submit(self):
        raise NotImplementedError()

    def __update_fields_state(self, state: bool):
        """
        Habilita/desabilita os campos do formulário
        """

        fields = self.query(FormField)
        for field in fields:
            field.disabled = not state

    def __update_submit_state(self):
        """
        Altera o estado do botão caso o formulário esteja preenchido
        """

        self.query_one(".submit", Button).disabled = not self.__is_form_filled()

    def __is_form_filled(self):
        """
        Verifica se todos os campos do formulário estão válidos
        """

        fields = self.query(FormField)
        return all(field.is_valid() for field in fields)

    def _get_values(self):
        """
        Coloca todos os campos do formulário em um dicionário
        """

        values = {}
        for field in self.query(FormField):
            values[field.id] = field.value
        return values
