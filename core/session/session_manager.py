from uuid import UUID

from core.models import Session


class SessionManager:
    """Classe responsável por gerenciar as sessões"""

    def __init__(self):
        self._session: Session | None = None

    @property
    def is_authenticated(self) -> bool:
        """Verifica se a sessão atual é válida"""
        return self._session is not None

    @property
    def current_session(self):
        """Retorna a sessão atual"""
        return self._session

    def start(self, user_id: UUID):
        """Vincula à uma sessão a partir de um id de usuário"""
        self._session = Session(user_id=user_id)

    def end(self):
        """Desvincula a sessão atual"""
        self._session = None
