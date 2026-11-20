from textual.widget import Widget

from tui.modals.profile_modal import ProfileModal
from tui.widgets.alt_image import AltImage


class Profile(Widget):
    def __init__(self):
        super().__init__(
            classes="modal_controller",
        )

    def compose(self):
        yield AltImage(image=self.app.profile.photo, alt="👤")

    def on_click(self):
        modal = self.screen.query_one(ProfileModal)
        modal.toggle()
