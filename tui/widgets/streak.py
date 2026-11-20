from textual.widget import Widget
from textual.widgets import Static


class Streak(Widget):
    def compose(self):
        streak = self.app.gamification_profile.streak
        self.classes = 'active' if streak > 0 else ''
        yield Static(f"{'🔥' if streak > 0 else '🧊'} {streak} dias")
