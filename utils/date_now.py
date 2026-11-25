from datetime import datetime, timezone


def date_now():
    """Retorna a data e hora atual em UTC"""
    return datetime.now(tz=timezone.utc).isoformat()
