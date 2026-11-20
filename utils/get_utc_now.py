from datetime import datetime, timezone


def get_utc_now():
    """
    Retorna a data e hora atual no fuso horário UTC.
    """

    return datetime.now(tz=timezone.utc)
