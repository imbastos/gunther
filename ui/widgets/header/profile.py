from textual.widget import Widget

from ui.widgets.alt_image import AltImage


class Profile(Widget):
    """Botão de perfil no cabeçalho que abre o dropdown do usuário."""

    def __init__(self):
        super().__init__(classes="bg-surface hover center square-3 ml-2")

    def compose(self):
        current_user = getattr(self.screen, "current_user", None)
        avatar = (
            current_user.image
            if current_user is not None and current_user.image
            else "assets/icon.png"
        )
        yield AltImage(image=avatar, alt="👤")

    def on_click(self):
        from ui.modals.profile_dropdown import ProfileDropdown

        modal = self.screen.query_one(ProfileDropdown)
        modal.toggle()
