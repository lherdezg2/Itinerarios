import unicodedata


def normalize_search_text(value: str) -> str:
    """Normaliza texto para busqueda: minusculas y sin tildes."""
    folded = unicodedata.normalize("NFD", value.strip())
    without_marks = "".join(
        character for character in folded if unicodedata.category(character) != "Mn"
    )
    return without_marks.lower()
