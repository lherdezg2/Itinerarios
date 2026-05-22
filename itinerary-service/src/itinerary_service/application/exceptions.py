class UpstreamAirportServiceError(Exception):
    """Fallo al consultar el Airport Service (red o respuesta inesperada)."""


class ItineraryNotFoundError(Exception):
    """Itinerario no encontrado por itinerary_id."""

