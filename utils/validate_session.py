from core.exceptions.auth_exception import NotAuthorizedError
from core.models.session import Session


def validate_session(session: Session | None) -> Session:
    if isinstance(session, Session):
        return session
    raise NotAuthorizedError()
