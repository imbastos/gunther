from typing import Any


def format_collection_items(items: Any, empty_message: str) -> str:
    """Formata coleções de exemplos e referências."""

    if not items:
        return empty_message

    if isinstance(items, dict):
        return "\n".join(f"• {key}: {value}" for key, value in items.items())

    if isinstance(items, list):
        lines = []

        for index, item in enumerate(items, 1):
            if not isinstance(item, dict):
                lines.append(f"• {item}")
                continue

            title = item.get("title") or item.get("name") or f"Item {index}"
            details = [
                f"{key}: {value}"
                for key, value in item.items()
                if key not in ("title", "name") and value is not None
            ]

            lines.append(
                f"{index}. {title}"
                + ("\n   " + "\n   ".join(details) if details else "")
            )

        return "\n".join(lines)

    return str(items)
