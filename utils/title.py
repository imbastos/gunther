import pyfiglet


def title(text: str, font: str = "rectangles") -> str:
    """Gera um título estilizado usando pyfiglet"""
    formatted = pyfiglet.figlet_format(text, font=font)
    return "\n".join(formatted.splitlines()[:-1])
