class Error(Exception):
    """Classe base para todas as exceções personalizadas"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
