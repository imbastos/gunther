import os

from PIL import UnidentifiedImageError
from textual.widget import Widget
from textual.widgets import Static
from textual_image.widget import Image


class AltImage(Widget):
    """Widget para exibir imagem no terminal com fallback textual."""

    def __init__(self, image: str | None, alt: str = "🖼", classes: str = ""):
        super().__init__(classes=f"w-1--1 h-1--1 {classes}")
        self.image = image
        self.alt = alt

    def _make_fallback(self) -> Static:
        return Static(self.alt, classes="content-center text-center w-1--1 h-1--1")

    def _image_accessible(self) -> bool:
        """Verifica se a imagem existe e é acessível antes de tentar carregá-la."""
        if not self.image:
            return False
        if self.image.startswith(("http://", "https://")):
            return True
        return os.path.isfile(self.image)

    def compose(self):
        if self.app.use_images and self._image_accessible():
            try:
                yield Image(
                    image=self.image,
                    classes="w-1--1 h-1--1",
                    on_error=lambda _: self._make_fallback(),
                )
                return
            except (FileNotFoundError, OSError, ValueError, EOFError, UnidentifiedImageError):
                pass

        yield self._make_fallback()
