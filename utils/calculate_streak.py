from datetime import datetime

from utils.date_now import date_now
from utils.parse_datetime import parse_datetime


def calculate_streak(
    streak: int,
    last_activity: datetime | str | None,
    now: datetime | str | None = None,
) -> int:
    last_activity = parse_datetime(last_activity)
    current = parse_datetime(now or date_now())

    if last_activity is None or current is None:
        return 1

    if last_activity.tzinfo is None:
        current = current.replace(tzinfo=None)
    elif current.tzinfo is None:
        last_activity = last_activity.replace(tzinfo=None)

    days = (current.date() - last_activity.date()).days

    if days == 0:
        return streak

    if days <= 2:
        return streak + 1

    return 1
