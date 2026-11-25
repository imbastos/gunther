from datetime import datetime


def parse_datetime(value: datetime | str | None) -> datetime | None:
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
