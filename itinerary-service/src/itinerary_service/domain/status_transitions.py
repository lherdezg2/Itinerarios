from itinerary_service.domain.itinerary import ItineraryStatus


class InvalidStatusTransitionError(ValueError):
    """Transicion de estado no permitida por las reglas de negocio (HU-C3)."""


_ALLOWED_TRANSITIONS: frozenset[tuple[ItineraryStatus, ItineraryStatus]] = frozenset(
    {
        (ItineraryStatus.PENDIENTE, ItineraryStatus.EN_CURSO),
        (ItineraryStatus.PENDIENTE, ItineraryStatus.COMPLETADO),
        (ItineraryStatus.EN_CURSO, ItineraryStatus.COMPLETADO),
    }
)


def apply_status_change(current: ItineraryStatus, new: ItineraryStatus) -> ItineraryStatus:
    if current == ItineraryStatus.COMPLETADO:
        raise InvalidStatusTransitionError(
            "No se puede cambiar el estado de un itinerario completado."
        )
    if (current, new) not in _ALLOWED_TRANSITIONS:
        raise InvalidStatusTransitionError(
            f"Transicion no valida de '{current.value}' a '{new.value}'."
        )
    return new
