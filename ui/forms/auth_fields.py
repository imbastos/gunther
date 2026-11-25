from textual.validation import Length, Regex

from ui.widgets import FormField


def username():
    return FormField(
        id="username",
        placeholder="Nome de usuário",
        validators=[
            Length(
                minimum=3,
                maximum=64,
                failure_description="tamanho inválido",
            ),
        ],
    )


def email():
    return FormField(
        id="email",
        placeholder="E-mail",
        validators=[
            Regex(
                r"(?i)^[a-z0-9.]+@[a-z0-9]+\.[a-z]+(\.[a-z]+)?$",
                failure_description="formato inválido",
            ),
        ],
    )


def password():
    return FormField(
        id="password",
        placeholder="Senha",
        password=True,
        validators=[
            Length(
                minimum=8,
                failure_description="mínimo de 8 caracteres",
            ),
        ],
    )
