import os
import shutil
from uuid import UUID, uuid4


def copy_user_photo(source_path: str, user_id: UUID | str) -> str:
    """Copia a imagem selecionada do computador para assets/upload/ e retorna o caminho relativo."""
    cleaned = source_path.strip().strip('"').strip("'")
    if not cleaned or not os.path.isfile(cleaned):
        raise FileNotFoundError(f"Arquivo não encontrado: {source_path}")

    upload_dir = os.path.join("assets", "upload")
    os.makedirs(upload_dir, exist_ok=True)

    _, ext = os.path.splitext(cleaned)
    filename = f"{user_id}_{uuid4().hex[:8]}{ext or '.png'}"
    dest_path = os.path.join(upload_dir, filename)
    shutil.copy2(cleaned, dest_path)
    return f"assets/upload/{filename}"
