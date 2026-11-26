from textual import on
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class GameModal(ModalScreen):
    def __init__(self):
        super().__init__()

    def compose(self):
        with Vertical(classes="w-1--3"):
            yield Label("[$primary]Como funciona?", classes="text-center w-1--1 mb-2")
            yield Label(
                """No [$primary]ArchKata[/$primary], seu objetivo é projetar uma arquitetura que atenda aos requisitos de cada desafio.\n
Você possui um orçamento limitado para comprar e conectar nós (nodes), como servidores, bancos de dados e load balancers. [bold]Cada nó possui custos e características próprias.[/bold]\n
Escolha os componentes certos, gerencie seu orçamento e monte uma arquitetura capaz de cumprir todos os requisitos!\n
[bold]Planeje, conecte e construa a solução ideal!""",
                classes="text-center w-1--1 mb-1",
            )

            yield Button("Entendi", classes="w-full", id="dismiss")

    @on(Button.Pressed, "#dismiss")
    def handle_dismiss(self):
        self.dismiss()
