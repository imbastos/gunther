import os

from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import DirectoryTree, Label

from ui.widgets.action_button import ActionButton


class FilePickerModal(ModalScreen[str | None]):
    """Modal para selecionar uma foto no computador."""

    def __init__(self, start_path: str | None = None):
        super().__init__()
        self.start_path = start_path or os.path.expanduser("~")

    def compose(self):
        with (
            Container(classes="center-container"),
            Vertical(id="file-picker-dialog", classes="w-48 bg-surface round-panel p-1-2"),
        ):
            yield Label("Selecionar foto", classes="text-bold mb-1")
            yield DirectoryTree(
                self.start_path,
                id="file-picker-tree",
                classes="w-full h-10 mb-1",
            )
            yield ActionButton(
                "Cancelar",
                action=lambda: self.dismiss(None),
                id="file-picker-cancel",
                classes="h-3 border-none bg-panel p-0-2 w-full",
            )

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        self.dismiss(str(event.path))
