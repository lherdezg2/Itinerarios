from itinerary_service.application.status_codes import status_to_api
from itinerary_service.domain.itinerary import ItineraryStatus

API_STATUS_PENDING = "PENDING"
API_STATUS_IN_PROGRESS = "IN_PROGRESS"
API_STATUS_COMPLETED = "COMPLETED"


class InvalidStatusTransitionError(ValueError):
    """Transicion de estado no permitida (HU-C3)."""


_ALLOWED_TRANSITIONS: dict[str, list[str]] = {
    API_STATUS_PENDING: [API_STATUS_IN_PROGRESS, API_STATUS_COMPLETED],
    API_STATUS_IN_PROGRESS: [API_STATUS_COMPLETED],
    API_STATUS_COMPLETED: [],
}


def is_valid_api_transition(current: str, new: str) -> bool:
    return new in _ALLOWED_TRANSITIONS.get(current, [])


def ensure_valid_status_transition(current: ItineraryStatus, new: ItineraryStatus) -> None:
    current_api = status_to_api(current)
    new_api = status_to_api(new)
    if not is_valid_api_transition(current_api, new_api):
        raise InvalidStatusTransitionError(
            f"Transicion no valida de '{current_api}' a '{new_api}'."
        )
