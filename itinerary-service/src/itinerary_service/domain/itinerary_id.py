import re

ITINERARY_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


def normalize_itinerary_id(itinerary_id: str | None) -> str | None:
    if itinerary_id is None:
        return None
    cleaned = itinerary_id.strip()
    if not cleaned:
        return None
    if not ITINERARY_ID_PATTERN.fullmatch(cleaned):
        raise ValueError(
            "itinerary_id invalido. Use 1-64 caracteres alfanumericos, guion o guion bajo."
        )
    return cleaned
