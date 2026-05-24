from itinerary_service.application.status_codes import (
    API_STATUS_COMPLETED,
    API_STATUS_IN_PROGRESS,
    API_STATUS_PENDING,
    status_to_api,
)
from itinerary_service.domain.itinerary import ItineraryStatus

_EDITABLE_API_STATUSES = frozenset({API_STATUS_PENDING, API_STATUS_IN_PROGRESS})


class ItineraryEditNotAllowedError(Exception):
    """El estado del itinerario no permite edicion (HU-B5)."""


def ensure_itinerary_editable(status: ItineraryStatus) -> None:
    current = status_to_api(status)
    if current in _EDITABLE_API_STATUSES:
        return
    if current == API_STATUS_COMPLETED:
        raise ItineraryEditNotAllowedError("No se puede editar un itinerario completado.")
    raise ItineraryEditNotAllowedError("El estado del itinerario no permite edicion.")
