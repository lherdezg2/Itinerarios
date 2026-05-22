from itinerary_service.domain.itinerary import ItineraryStatus

API_STATUS_PENDING = "PENDING"
API_STATUS_IN_PROGRESS = "IN_PROGRESS"
API_STATUS_COMPLETED = "COMPLETED"

API_TO_DOMAIN: dict[str, ItineraryStatus] = {
    API_STATUS_PENDING: ItineraryStatus.PENDIENTE,
    API_STATUS_IN_PROGRESS: ItineraryStatus.EN_CURSO,
    API_STATUS_COMPLETED: ItineraryStatus.COMPLETADO,
}

DOMAIN_TO_API: dict[ItineraryStatus, str] = {value: key for key, value in API_TO_DOMAIN.items()}


def parse_api_status(value: object) -> ItineraryStatus:
    if not isinstance(value, str):
        raise ValueError("El campo status es obligatorio y debe ser texto.")
    code = value.strip().upper()
    if code not in API_TO_DOMAIN:
        allowed = ", ".join(sorted(API_TO_DOMAIN))
        raise ValueError(f"Status no permitido. Valores validos: {allowed}.")
    return API_TO_DOMAIN[code]


def status_to_api(status: ItineraryStatus) -> str:
    return DOMAIN_TO_API.get(status, status.value)
